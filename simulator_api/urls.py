from django.urls import path

from .views import *

urlpatterns = [
    path('simulator/create', SimulatorCreation.as_view(), name="Simulator"),
    path('simulator/list', SimulatorListing.as_view(), name="Simulator"),
    path('simulator/run', SimulatorRunning.as_view(), name="run"),
    path('simulator/stop', SimulatorStopping.as_view(), name="stop"),

]
