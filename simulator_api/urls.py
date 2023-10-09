from django.urls import path

from .views import *

urlpatterns = [
    path('simulators/', SimulatorListing.as_view(), name="SimulatorListing"),
    path('simulator/', SimulatorCreation.as_view(), name="SimulatorCreation"),
    path('run_simulator/<str:simulator_name>', SimulatorRunning.as_view(), name="run"),
    path('stop_simulator/<str:simulator_name>', SimulatorStopping.as_view(), name="stop"),
]
