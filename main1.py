import json
import subprocess

# Read config.json
with open('config.json') as config_file:
    config_data = json.load(config_file)


common_variables = config_data["common_variables"]
_PG_SERVER_ENCODING = common_variables["_PG_SERVER_ENCODING"]
_PG_SERVER_REPLICATION_USERNAME = common_variables["_PG_SERVER_REPLICATION_USERNAME"]
_PG_SERVER_REPLICATION_USER_PASSWORD = common_variables["_PG_SERVER_REPLICATION_USER_PASSWORD"]
_PG_CIRRUS_CONF_DIRECTORY = common_variables["_PG_CIRRUS_CONF_DIRECTORY"]
_PG_SERVER_VERSION = common_variables["_PG_SERVER_VERSION"]


# Extract required values
ansible_host = config_data['_PG_SERVER_PRIMARY_IP']
ansible_connection = "ssh"
ansible_user = config_data['_PG_SERVER_PRIMARY_USERNAME']
ansible_become_pass = config_data['_PG_SERVER_PRIMARY_PSSWD']

# Define extra variables
extra_vars = {
    "_PG_PORT": config_data['_PG_PORT'],
    "_PG_PASSWORD": config_data['_PG_PASSWORD'],
    "_PG_VERSION": config_data['_PG_VERSION'],
    "_PG_CIRRUS_DIRECTORY": config_data['_PG_CIRRUS_DIRECTORY'],
    "_PG_PRIMARY_DATA_DIRECTORY_NAME": config_data['_PG_PRIMARY_DATA_DIRECTORY_NAME'],
    "_PG_STANDBY1_DATA_DIRECTORY_NAME": config_data['_PG_STANDBY1_DATA_DIRECTORY_NAME'],
    "_PG_STANDBY2_DATA_DIRECTORY_NAME": config_data['_PG_STANDBY2_DATA_DIRECTORY_NAME']
}

# Execute Ansible playbook
command = [
    'ansible-playbook',
    '-i', ansible_host + ',',
    '-e', f'ansible_connection={ansible_connection}',
    '-e', f'ansible_user={ansible_user}',
    '-e', f'ansible_become_pass={ansible_become_pass}',
    'playbook.yml'
]

# Extend command with extra variables
for key, value in extra_vars.items():
    command.extend(['-e', f'{key}={value}'])

subprocess.run(command)

