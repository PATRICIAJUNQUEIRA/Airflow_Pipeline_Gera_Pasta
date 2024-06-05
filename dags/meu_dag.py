from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import logging
import pandas as pd
from os.path import join
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def extrai_dados(execution_date, city, key, base_path):
    folder_path = join(base_path, f'pasta_{execution_date}')
    try:
        os.makedirs(folder_path, exist_ok=True)
        logger.info(f"Folder created at: {folder_path}")

        # Montagem da URL para a API de dados meteorológicos
        URL = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{execution_date}?unitGroup=metric&include=days&key={key}&contentType=csv'
        logger.info(f'Downloading data from: {URL}')
        data = pd.read_csv(URL)

        # Salvando os dados
        data_file_path = join(folder_path, 'weather_data.csv')
        data.to_csv(data_file_path, index=False)
        logger.info(f"Data saved at: {data_file_path}")
        
    except Exception as e:
        logger.error(f"Failed to download or save data: {e}")

with DAG(
    'dag_patricia',
    start_date=days_ago(1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    tarefa_1 = EmptyOperator(task_id='tarefa_1')
    tarefa_2 = EmptyOperator(task_id='tarefa_2')
    tarefa_3 = EmptyOperator(task_id='tarefa_3')

    cria_pasta = BashOperator(
        task_id='create_folder',
        bash_command='mkdir -p "/home/patricia/Documentos/airflow/pasta_{{ ds }}"'
    )

    extract_data = PythonOperator(
        task_id='extract_data',
        python_callable=extrai_dados,
        op_kwargs={
            'execution_date': '{{ ds }}',
            'city': 'Boston',
            'key': 'LBGDWPHK4ZVDH8AJL5KDVAJC5',
            'base_path': '/home/patricia/Documentos/airflow'
        }
    )

    tarefa_1 >> [tarefa_2, tarefa_3]
    tarefa_3 >> cria_pasta
    cria_pasta >> extract_data