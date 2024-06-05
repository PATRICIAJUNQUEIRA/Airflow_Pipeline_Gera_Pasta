import os
from os.path import join
import pandas as pd 
from datetime import datetime, timedelta

# Intervalo de datas
data_inicio = datetime.today()
data_fim = data_inicio + timedelta(days=7)

#Formatando as Datas
data_inicio = data_inicio.strftime('%Y-%m-%d')
data_fim = data_fim.strftime('%Y-%m-%d')

city = 'Boston'
Key = 'LBGDWPHK4ZVDH8AJL5KDVAJC5'

URL = join('https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/',
           f'{city}/{data_inicio}/{data_fim}?unitGroup=metric&include=days&key={Key}&contentType=csv')

dados = pd.read_csv(URL)
print(dados.head())

file_path = f'/home/patricia/Documentos/DataPipeline/semana={data_inicio}/'
os.mkdir(file_path)

dados.to_csv(file_path + 'dados_brutos.csv')
dados[['datetime', 'tempmin', 'temp', 'tempmax']].to_csv(file_path + 'temperaturas.csv')
dados[['datetime', 'description', 'icon']].to_csv(file_path + 'condicoes.csv')

#Pipeline que cria uma pasta com a data de inicio da extração na qual são armazenados
# os dados  extraídos nos 7 dias a frente desta data. 