#!bin/sh
nohup airflow scheduler &
airflow webserver &
python3 API.py