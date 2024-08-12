
from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=30),
}
with DAG(
    'weather',
    default_args=default_args,
    description='Schedule Weather Ingestion',
    schedule_interval="58 * * * *",
    start_date=datetime.today() - timedelta(days=1),
    catchup=False
) as dag:

    t1 = BashOperator(
        task_id='import_weather_data_to_csv',
        bash_command='python /opt/airflow/dags/weather_data_ingestion.py --date {{ ds }}'
    )
    t2 = BashOperator(
        task_id='export_data_to_db',
        bash_command='python /opt/airflow/dags/weather_to_db.py '
                     '--date {{ ds }} --connection %s' % Variable.get("data_dev_connection")
    )

    t1 >> t2