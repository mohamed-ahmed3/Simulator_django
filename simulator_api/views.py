from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import viewsets

from simulator_api.models import *
from simulator_api.serializers import *


class ConfigurationView(ListCreateAPIView):
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer
    pagination_class = PageNumberPagination


class SimulatorView(ListCreateAPIView):
    queryset = Simulator.objects.all()
    serializer_class = SimulatorSerializer
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        end_date = serializer.validated_data.get('end_date')
        data_size = serializer.validated_data.get('data_size')

        if not end_date and not data_size:
            return Response({'detail': 'Even one of end_date or data_size should have a value.'}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        return Response({'detail': 'Simulator created successfully.'}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

        data = self.request.data
        configurations_data = data.pop('configurations', [])
        simulator = serializer.instance

        for config_data in configurations_data:
            config_serializer = ConfigurationSerializer(data=config_data)
            if config_serializer.is_valid():
                config_serializer.save(simulator=simulator)
            else:
                pass
