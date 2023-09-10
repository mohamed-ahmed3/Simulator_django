from django.urls import path

from .views import *

urlpatterns = [
    path('configurator/', ConfigurationView.as_view(), name="Configuration"),
    path('simulator/', SimulatorView.as_view(), name="Simulator")

]
