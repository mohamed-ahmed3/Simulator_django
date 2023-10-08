import os

from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
import threading, time
import json
import csv

from configuration_manager_creator import ConfigurationManagerCreator
from data_simulator import DataGenerator
from data_producer import DataProducerFileCreation
from .serializers import *


class SimulatorListing(ListCreateAPIView):
    queryset = Simulator.objects.all()
    serializer_class = SimulatorSerializer
    pagination_class = PageNumberPagination


class SimulatorCreation(ListCreateAPIView):
    """
    View for creating and listing simulator instances and associated data.

    This view allows creating a new simulator instance along with its configuration data,
    such as datasets and seasonality components. It also provides listing functionality for existing
    simulator instances.

    Attributes:
        queryset (QuerySet): The set of Simulator objects to be queried.
        serializer_class (Serializer): The serializer class used for serializing and deserializing data.
        pagination_class (Pagination): The pagination class for controlling the response data's structure.

    Methods:
        create(request, *args, **kwargs): Handles the creation of a new simulator instance and associated data.
                                         Validates and processes the input data, performs the creation, and returns
                                         an appropriate response.

    """
    serializer_class = SimulatorSerializer
    pagination_class = PageNumberPagination

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Create a new simulator instance and associated data.

        This method handles the creation of a new simulator instance along with its configuration data,
        such as datasets and seasonality components. It first validates the input data, including the simulator
        details and associated configurations. If the data is valid, it performs the creation of the simulator
        instance and related data. If any validation errors occur or if the creation process fails, it returns
        an appropriate error response.

        Arguments:
            request (HttpRequest): The HTTP request object containing the data to create the simulator instance.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A response object with details about the created simulator and related data, or an error
                      response if the creation process encounters issues.

        Raises:
            HTTPException: Raises exceptions for various HTTP error responses, such as bad requests or conflicts.

        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        configuration_data = request.data.pop('datasets', [])
        seasonality_data = request.data.pop('seasonality_components', [])

        self.perform_create(serializer)

        simulator = serializer.instance
        print(simulator.status)
        for config_data in configuration_data:
            config_serializer = ConfigurationSerializer(data=config_data)

            if config_serializer.is_valid():
                config_instance = config_serializer.save(simulator=simulator)

            else:
                pass

            config_instance.save()

        for season_data in seasonality_data:
            season_serializer = SeasonalitySerializer(data=season_data)
            if season_serializer.is_valid():
                season_serializer.save(
                    config=simulator)
            else:
                pass

        return Response({'detail': 'Simulator and related data created successfully.'},
                        status=status.HTTP_201_CREATED)


simulator_threads = {}
stop_simulator_flags = {}


class SimulatorRunning(APIView):
    @transaction.atomic
    def post(self, request, simulator_name):
        """
        Start running a simulator in the background.

        This method handles the initiation of a simulator's execution in a separate thread. It checks if the provided
        simulator name exists, then runs the simulator's data generation process in the background thread.
        The simulator's status is updated accordingly during execution. If any errors occur, the status is set to "Failed".

        Arguments:
            request (HttpRequest): The HTTP request object containing the simulator's name in the POST data.

        Returns:
            Response: A response indicating that the simulator is running or an error response if the simulator
                      is not found or if an error occurs during execution.

        """
        try:
            simulator = Simulator.objects.get(name=simulator_name)
        except Simulator.DoesNotExist:
            return Response(
                {"error": f"Simulator with name '{simulator_name}' not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        def run_simulator_in_background(simulator):
            simulator.status = "Running"
            simulator.save()

            stop_simulator_flags[simulator.process_id] = threading.Event()
            try:
                print(simulator.status)
                configuration_manager = ConfigurationManagerCreator.create("db", simulator.name)
                data_simulator = DataGenerator(configuration_manager)
                csv_file_name = f"{simulator.name}_data.csv"
                csv_file_path = os.path.join('sample_datasets', csv_file_name)
                meta_data_producer = DataProducerFileCreation.create(csv_file_path)

                meta_data = []
                for (data, meta_data_point) in data_simulator.generate():
                    if stop_simulator_flags[simulator.process_id].is_set():
                        del stop_simulator_flags[simulator.process_id]
                        return
                    DataProducerFileCreation.create(f"sample_datasets/{meta_data_point['id']}").produce(data)
                    meta_data.append(meta_data_point)

                meta_data_producer.produce(meta_data)

                data = []
                with open(csv_file_path, 'r') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    for row in csv_reader:
                        data.append(row)

                data_json = json.dumps(data)
                simulator.metadata = data_json
                simulator.status = "Succeeded"
                simulator.save()
                print(simulator.status)

            except Exception as e:
                simulator.status = "Failed"
                simulator.save()
                print(str(e))
                return Response({simulator.name: "failed"}, status=status.HTTP_200_OK)

            finally:
                if simulator.process_id in simulator_threads:
                    del simulator_threads[simulator.process_id]
                    del stop_simulator_flags[simulator.process_id]
            time.sleep(1)

        simulator_thread = threading.Thread(target=run_simulator_in_background, args=(simulator,))
        simulator_threads[simulator.process_id] = simulator_thread
        simulator_thread.daemon = True
        simulator_thread.start()

        return Response({simulator.name: "Running"}, status=status.HTTP_200_OK)


class SimulatorStopping(APIView):
    """
    Stop a running simulator.

    This method handles the request to stop a simulator's execution. It checks if the provided simulator name exists
    and whether the simulator is currently running in a background thread. If found, it signals the thread to stop,
    waits for the thread to complete, and updates the simulator's status to "Failed". If the simulator is not running,
    it returns a message indicating that the simulator was not running.

    Arguments:
        request (HttpRequest): The HTTP request object containing the simulator's name in the POST data.

    Returns:
        Response: A response indicating the status of the simulator's stopping process or an error response if the
                  simulator is not found or if it was not running.

    """

    @transaction.atomic
    def post(self, request, simulator_name):

        if not simulator_name:
            return Response(
                {"error": "Simulator name is required in the POST data."},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            try:
                simulator = Simulator.objects.get(name=simulator_name)
                simulator_thread = simulator_threads.get(simulator.process_id)

                if simulator_thread:
                    stop_simulator_flags[simulator.process_id].set()

                    simulator_thread.join()

                    simulator.status = "Failed"
                    simulator.save()

                    return Response({"message": f"{simulator_name} stopped."},
                                    status=status.HTTP_200_OK)

                else:
                    return Response({"message": f"{simulator_name} was not running."},
                                    status=status.HTTP_200_OK)
            except Simulator.DoesNotExist:
                return Response(
                    {"error": f"Simulator with name '{simulator_name}' not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
