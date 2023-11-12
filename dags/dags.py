from airflow import DAG
from airflow.operators.python import PythonOperator
import datetime
import sys
import os
import django

sys.path.insert(1, '/opt/airflow/simulator_files')
sys.path.insert(1, '/opt/airflow/simulator_files/simulator')

django.setup()

from simulator_api.views import *
from simulator_api.models import *


MY_NAME = "Hassan"


def create_dag(simulator_name):
    def python_callable():
        view_instance = SimulatorRunning()
        view_instance.post("test", simulator_name)

    with DAG(
            dag_id=simulator_name,
            catchup=False,
            start_date=datetime.datetime(2023, 11, 12),
            tags=["tutorial"],
            default_args={
                "owner": MY_NAME,
                "retries": 1,
            }
    ) as dag:

        t1 = PythonOperator(
            task_id=f"run_{simulator_name}",
            python_callable=python_callable,
        )


simulator_instance = SimulatorListing
simulators = Simulator.objects.all()

for simulator in simulators:
    create_dag(simulator.name)


