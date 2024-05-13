# Pipeline de Dados de Previsão do Tempo para Turismo

Este projeto desenvolve um pipeline de dados automatizado para uma empresa de turismo. O objetivo principal é extrair dados de previsão do tempo para a semana atual e armazená-los de maneira organizada para análises futuras.

## Visão Geral

O pipeline de dados foi criado para automatizar a extração de dados meteorológicos, utilizando a "Timeline Weather API" da Visual Crossing. O processo assegura que os dados mais recentes estejam sempre disponíveis para análise e planejamento estratégico pela empresa de turismo.

## Funcionalidades

- **Extração Automatizada**: Os dados são extraídos automaticamente da API "Timeline Weather API" do site [Visual Crossing](https://www.visualcrossing.com).
- **Armazenamento Organizado**: Os dados são armazenados em pastas, organizados por data de extração.
- **Agendamento Flexível**: O pipeline é configurado inicialmente para rodar automaticamente uma vez por dia. No entanto, este agendamento pode ser ajustado para uma execução semanal ou quinzenal conforme a regra de negócio da empresa.

## Tecnologias Utilizadas

- Python para scripting e automação.
- Airflow para orquestração e agendamento do pipeline.
- APIs da Visual Crossing para extração de dados.

## Configuração e Instalação

Para configurar e instalar o pipeline em seu ambiente local, siga estes passos:

1. Clone o repositório do projeto: git clone https://github.com/PATRICIAJUNQUEIRA/Airflow_Pipeline_Gera_Pasta.git
2. Instale as dependências necessárias (preferencialmente em um ambiente virtual):
   pip install -r requirements.txt
3. Configure o Airflow e inicialize o ambiente:
  airflow initdb
  airflow webserver -p 8080
4. Configure a conexão com a API "Timeline Weather API" no Airflow.

## Uso

Para executar o pipeline, ative a DAG correspondente no painel do Airflow. Ajuste o agendamento conforme necessário para atender às demandas específicas da empresa, seja diariamente, semanalmente ou quinzenalmente.

## Imagens e Visualizações

### Diagrama de Tarefas no Airflow
![image](https://github.com/PATRICIAJUNQUEIRA/Airflow_Pipeline_Gera_Pasta/assets/96187596/314eb17a-5e6b-4d0d-8ccf-0958eb70e165)


### Calendário de Execuções no Airflow
![image](https://github.com/PATRICIAJUNQUEIRA/Airflow_Pipeline_Gera_Pasta/assets/96187596/3e7776b2-fd3d-481e-8713-f3d838bb6820)

## Contribuições

Contribuições são bem-vindas! Para contribuir com o projeto, faça um fork do repositório, crie uma nova branch, faça suas alterações e envie um pull request.



