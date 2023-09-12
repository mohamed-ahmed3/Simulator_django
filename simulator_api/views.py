from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
import threading, time
from django.http import StreamingHttpResponse

from configuration_manager import ConfigurationManagerCreator
from data_simulator import DataGenerator
from data_producer import DataProducerFileCreation
from .serializers import *


class SeasonalityView(ListCreateAPIView):
    queryset = SeasonalityComponentDetails.objects.all()
    serializer_class = SeasonalitySerializer
    pagination_class = PageNumberPagination


class ConfigurationView(ListCreateAPIView):
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        seasonality_data = request.data.pop('seasonality_components', [])

        self.perform_create(serializer)

        configuration = serializer.instance

        for season_data in seasonality_data:
            season_serializer = SeasonalitySerializer(data=season_data)
            if season_serializer.is_valid():
                season_serializer.save(
                    config=configuration)
            else:
                pass

        return Response({'detail': 'Simulator and related data created successfully.'},
                        status=status.HTTP_201_CREATED)


class SimulatorView(ListCreateAPIView):
    queryset = Simulator.objects.all()
    serializer_class = SimulatorSerializer
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        configuration_data = request.data.pop('datasets', [])
        seasonality_data = request.data.pop('seasonality_components', [])

        end_date = serializer.validated_data.get('end_date')
        data_size = serializer.validated_data.get('data_size')

        if not end_date and not data_size:
            return Response({'detail': 'Even one of end_date or data_size should have a value.'},
                            status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)

        simulator = serializer.instance
        print(simulator.status)
        for config_data in configuration_data:
            config_serializer = ConfigurationSerializer(data=config_data)
            if config_serializer.is_valid():
                config_serializer.save(simulator=simulator)
            else:
                pass

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
stop_simulator_flag = threading.Event()


class SimulatorRunning(APIView):
    def post(self, request):
        simulator_name = request.data.get("name")
        if not simulator_name:
            return Response(
                {"error": "Simulator name is required in the POST data."},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
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

                try:
                    print(simulator.status)
                    configuration_manager = ConfigurationManagerCreator.create("db.sqlite3", simulator_name)
                    data_simulator = DataGenerator(configuration_manager)
                    meta_data_producer = DataProducerFileCreation.create('sample_datasets/meta_data.csv')

                    meta_data = []
                    for (data, meta_data_point) in data_simulator.generate():
                        if stop_simulator_flag.is_set():
                            return
                        DataProducerFileCreation.create(f"sample_datasets/{meta_data_point['id']}").produce(data)
                        meta_data.append(meta_data_point)

                    meta_data_producer.produce(meta_data)

                    simulator.status = "Succeeded"
                    simulator.save()
                    print(simulator.status)

                except Exception as e:
                    simulator.status = "Failed"
                    simulator.save()
                    print(str(e))
                    return Response({simulator.name: "failed"}, status=status.HTTP_200_OK)

                time.sleep(1)

            simulator_thread = threading.Thread(target=run_simulator_in_background, args=(simulator,))
            simulator_threads[simulator.process_id] = simulator_thread
            simulator_thread.daemon = True
            simulator_thread.start()

            return Response({simulator.name: "Running"}, status=status.HTTP_200_OK)


class StopSimulator(APIView):
    def post(self, request):
        simulator_name = request.data.get("name")

        if not simulator_name:
            return Response(
                {"error": "Simulator name is required in the POST data."},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            try:
                simulator = Simulator.objects.get(name=simulator_name)
                simulator_thread = simulator_threads.get(simulator.process_id)

                print(simulator_threads)
                print(simulator_thread)

                if simulator_thread:
                    stop_simulator_flag.set()

                    simulator_thread.join()

                    del simulator_threads[simulator.process_id]

                    simulator.status = "Failed"
                    simulator.save()

                    return Response({"message": f"{simulator_name}' stopped."},
                                    status=status.HTTP_200_OK)

                else:
                    return Response({"message": f"Simulator '{simulator_name}' was not running."},
                                    status=status.HTTP_200_OK)
            except Simulator.DoesNotExist:
                return Response(
                    {"error": f"Simulator with name '{simulator_name}' not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
