from django.urls import path

from .views import *

urlpatterns = [
    path('simulator/create', SimulatorView.as_view(), name="Simulator"),
    path('simulator/list', SimulatorView.as_view(), name="Simulator"),
    path('simulator/run', SimulatorRunning.as_view(), name="run"),
    path('simulator/stop', StopSimulator.as_view(), name="stop"),

]
