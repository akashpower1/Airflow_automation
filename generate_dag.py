import yaml
from jinja2 import Environment, FileSystemLoader, Template
from datetime import datetime

# Load configuration from YAML file
with open('config.yaml') as f:
    config_data = yaml.safe_load(f)


# Load YAML file
with open('config.yaml', 'r') as file:
    config_str = file.read()

# Load Jinja environment
env = Environment(loader=FileSystemLoader('.'))

# Render variables first
template = Template(config_str)
config_str = template.render(variables=config_data['variables'])

config_data = yaml.safe_load(config_str)

# Define data to render the template
data = {
    'owner': 'your_name',
    'start_date': datetime.now().strftime('%Y-%m-%d'),
    'dag_id': 'example_dag',
    'schedule_interval': '0 0 * * *',  # Daily schedule
    'tasks': config_data['tasks'],
    'final_task_flows': config_data['final_task_flows'],
}

# Render the Jinja template
template = env.get_template('dag_template.j2')
rendered_dag = template.render(data)

# Write the rendered DAG code to a Python file
with open('example_dag.py', 'w') as f:
    f.write(rendered_dag)

print("DAG file 'example_dag.py' generated successfully.")
