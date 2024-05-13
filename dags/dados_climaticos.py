from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import pendulum
import logging
import pandas as pd
from os.path import join
from airflow.macros import ds_add

# Definindo o DAG
with DAG(
    'meu_dag',
    start_date=pendulum.datetime(2024, 5, 13, tz="UTC"),
    schedule='0 9 * * 1',  # Executa toda segunda-feira ás 09h00
) as dag:
    
    # Tarefa 1: EmptyOperator não realiza ação prática, apenas inicia o fluxo
    tarefa_1 = EmptyOperator(task_id='tarefa_1')
   
    # Tarefa 2: Segue o mesmo padrão da tarefa_1
    tarefa_2 = EmptyOperator(task_id='tarefa_2')
    
    # Tarefa 3: Segue o mesmo padrão da tarefa_1
    tarefa_3 = EmptyOperator(task_id='tarefa_3')

    # Tarefa para criar a pasta diariamente com a data de execução
    cria_pasta = BashOperator(
        task_id='Cria_pasta',
        bash_command='mkdir -p "/home/patricia/Documentos/airflow/pasta_{{ds}}"'
    )

    # Função para extrair dados climáticos
    def extrai_dados(execution_date):
        logging.basicConfig(level=logging.INFO)
        try:
            city = 'Boston'
            key = 'LBGDWPHK4ZVDH8AJL5KDVAJC5'
            # Montando a URL para consulta dos dados climáticos
            URL = join('https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/',
                       f'{city}/{execution_date}/{execution_date}?unitGroup=metric&include=days&key={key}&contentType=csv')
            logging.info(f'Baixando dados de {URL}')
            dados = pd.read_csv(URL)

            # Salvando os dados na pasta correspondente à data de execução
            file_path = f'/home/patricia/Documentos/airflow/pasta_{execution_date}/'
            logging.info(f'Salvando dados em {file_path}')
            dados.to_csv(file_path + 'dados_brutos.csv')
            dados[['datetime', 'tempmin', 'temp', 'tempmax']].to_csv(file_path + 'temperaturas.csv')
            dados[['datetime', 'description', 'icon']].to_csv(file_path + 'condicoes.csv')
        except Exception as e:
            logging.error(f"Erro durante a execução: {e}")

    # Tarefa para extrair e salvar os dados climáticos
    tarefa_extrai_dados = PythonOperator(
        task_id='extrai_dados',
        python_callable=extrai_dados,
        op_kwargs={'data_de_execucao': '{{ ds }}'}
    )

    # Definindo a ordem de execução das tarefas
    tarefa_1 >> [tarefa_2, tarefa_3]
    tarefa_3 >> cria_pasta
    cria_pasta >> tarefa_extrai_dados