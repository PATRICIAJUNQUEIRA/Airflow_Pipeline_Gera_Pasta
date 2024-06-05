from airflow import DAG 
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.macros import ds_add
import pendulum
from os.path import join
import pandas as pd

with DAG(
    "dag_patricia",
    start_date=pendulum.datetime(2024, 6, 5, tz="UTC"),
    schedule_interval='0 9 * * 3',
) as dag:

    tarefa_1 = BashOperator(
        task_id = 'cria_pasta',
        bash_command = 'mkdir -p "//home/patricia/Documentos/airflow/pasta={{data_interval_end.strftime("%Y-%m-%d")}}"'
    )

    def extrai_dados(data_interval_end):
        city = 'Boston'
        key = 'ANZQ5K8QQP8BXZ85F4ZEQ2FPK'

        URL = join('https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/',
            f'{city}/{data_interval_end}/{ds_add(data_interval_end, 7)}?unitGroup=metric&include=days&key={key}&contentType=csv')

        dados = pd.read_csv(URL)

        file_path = f'/home/patricia/Documentos/airflow/pasta={data_interval_end}/'

        dados.to_csv(file_path + 'dados_brutos.csv')
        dados[['datetime','tempmin', 'temp', 'tempmax']].to_csv(file_path + 'temperaturas.csv')
        dados[['datetime', 'description', 'icon']].to_csv(file_path + 'condicoes.csv')

    tarefa_2 = PythonOperator(
        task_id = 'extrai_dados',
        python_callable = extrai_dados,
        op_kwargs = {'data_interval_end': '{{data_interval_end.strftime("%Y-%m-%d")}}'}
    )

    tarefa_1 >> tarefa_2