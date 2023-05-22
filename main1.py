import json
import subprocess

# Read config.json
with open('config.json') as config_file:
    config_data = json.load(config_file)

common_variables = config_data["common_variables"]
primary_variables = config_data["primary_variables"]
standby_variables = config_data["standby_variables"]

# Extract required values
ansible_host = primary_variables['_PG_SERVER_PRIMARY_IP']
ansible_connection = 'ssh'
ansible_user = primary_variables['_PG_SERVER_PRIMARY_USERNAME']
ansible_become_pass = primary_variables['_PG_SERVER_PRIMARY_PSSWD']

# Define extra variables
extra_vars = {
    "_PG_SERVER_PRIMARY_PORT": primary_variables['_PG_SERVER_PRIMARY_PORT'],
    "_PG_PASSWORD": primary_variables['_PG_PASSWORD'],
    "_PG_VERSION": common_variables['_PG_SERVER_VERSION'],
    "_PG_CIRRUS_CONF_DIRECTORY": common_variables['_PG_CIRRUS_CONF_DIRECTORY'],
    "_PG_SERVER_PRIMARY_DATA_DIRECTORY": primary_variables['_PG_SERVER_PRIMARY_DATA_DIRECTORY']
}

# Execute Ansible playbook
command = [
    'ansible-playbook',
    '-i', ansible_host + ',',
    '-e', f'ansible_connection={ansible_connection}',
    '-e', f'ansible_user={ansible_user}',
    '-e', f'ansible_become_pass={ansible_become_pass}',
    'playbook.yml',
    '-vvv'
]

# Extend command with extra variables
for key, value in extra_vars.items():
    command.extend(['-e', f'{key}={value}'])

subprocess.run(command)













for standby_var in standby_variables:

    # Extract required values
    ansible_host = standby_var['_PG_SERVER_STANDBY_IP']
    ansible_connection = 'ssh'
    ansible_user = standby_var['_PG_SERVER_STANDBY_USERNAME']
    ansible_become_pass = standby_var['_PG_SERVER_STANDBY_PSSWD']

    # Define extra variables
    extra_vars = {
        "_PG_SERVER_STANDBY_PORT": standby_var['_PG_SERVER_STANDBY_PORT'],
        "_PG_VERSION": common_variables['_PG_SERVER_VERSION'],
        "_PG_CIRRUS_CONF_DIRECTORY": common_variables['_PG_CIRRUS_CONF_DIRECTORY'],
        "_PG_SERVER_STANDBY_DATA_DIRECTORY": standby_var['_PG_SERVER_STANDBY_DATA_DIRECTORY']
    }

    # Execute Ansible playbook
    command = [
        'ansible-playbook',
        '-i', ansible_host + ',',
        '-e', f'ansible_connection={ansible_connection}',
        '-e', f'ansible_user={ansible_user}',
        '-e', f'ansible_become_pass={ansible_become_pass}',
        'playbook1.yml',
	'-vvv'
    ]

    # Extend command with extra variables
    for key, value in extra_vars.items():
        command.extend(['-e', f'{key}={value}'])

    subprocess.run(command)
