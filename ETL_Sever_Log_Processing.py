# import the libraries

from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago

#defining DAG arguments

# You can override them on a per-task basis during operator initialization

default_args = {
    'owner': 'Melvyn Salvatierra',
    'start_date': days_ago(0),
    'email': ['melvyn.salvatierra@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# defining the DAG
# define the DAG
dag = DAG(
    'ETL_Sever_Access_Log_Processing',
    default_args=default_args,
    description='Produce log for ETL Pipeline',
    schedule_interval=timedelta(days=1),
)

# define the tasks
# define the first task
download = BashOperator(
    task_id='download',
    bash_command='curl -O https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Apache%20Airflow/Build%20a%20DAG%20using%20Airflow/web-server-access-log.txt',
    dag=dag,
)

extract = BashOperator(
    task_id='extract',
    bash_command='cut -d"#" -f1,4 web-sever-access-log.txt > /home/project/airflow/dags/extracted.txt',
    dag=dag,
)

# define the task 'transform'

transform = BashOperator(
    task_id='transform',
    bash_command='tr "[a-z]" "[A-Z]" < /home/project/airflow/dags/extracted.txt > /home/project/airflow/dags/capitalized.txt',
    dag=dag,
)

# define the task 'load'

load = BashOperator(
    task_id='load',
    bash_command='zip log.zip capitalized.txt' ,
    dag=dag,
)
# task pipeline
download >> extract >> transform >> load
