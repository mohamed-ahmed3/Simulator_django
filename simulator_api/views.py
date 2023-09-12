from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

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


class SimulatorRunning(APIView):
    def post(self, request):
        # Get the simulator name from the request data
        simulator_name = request.data.get("name")

        # Check if the simulator name is provided in the POST data
        if not simulator_name:
            return Response(
                {"error": "Simulator name is required in the POST data."},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            configuration_manager = ConfigurationManagerCreator.create("db.sqlite3", simulator_name)
            data_simulator = DataGenerator(configuration_manager)
            meta_data_producer = DataProducerFileCreation.create('sample_datasets/meta_data.csv')

            meta_data = []
            for (data, meta_data_point) in data_simulator.generate():
                DataProducerFileCreation.create(f"sample_datasets/{meta_data_point['id']}").produce(data)
                meta_data.append(meta_data_point)

            meta_data_producer.produce(meta_data)

            return Response({"running"}, status=status.HTTP_200_OK)


