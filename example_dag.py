from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.ssh_operator import SSHOperator
from airflow.utils.dates import datetime, timedelta
from airflow.utils.task_group import TaskGroup

default_args = {
    'owner': 'your_name',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'example_dag',
    default_args=default_args,
    description='Automated DAG generated using Jinja',
    schedule_interval='0 0 * * *',
)





# Individual task: task1


task1 = SSHOperator(
    task_id='task1',
    command='echo "Task 1, var1=value1"',
    ssh_conn_id='my_ssh_connection',
    dag=dag,
)




# Individual task: task2


task2 = BashOperator(
    task_id='task2',
    bash_command='echo "Task 2, var2=value2"',
    dag=dag,
    xcom_push=True,
    env={'AIRFLOW_CONN_my_connection_id': 'my_connection_id'}
)




# Task Group: group1
with TaskGroup('group1') as group1:
    
    # Task: task3
    
    
    task3 = SSHOperator(
        task_id='task3',
        command='echo "Task 3 in group 1, var1=value1"',
        ssh_conn_id='my_ssh_connection',
        dag=dag,
    )
    
    
    # Task: task4
    
    
    task4 = BashOperator(
        task_id='task4',
        bash_command='echo "Task 4 in group 1, var2=value2"',
        dag=dag,
        xcom_push=True,
        env={'AIRFLOW_CONN_my_connection_id': 'my_connection_id'}
    )
    
    
    
    task3 >> task4
    




task1 >> group1 >> task2
