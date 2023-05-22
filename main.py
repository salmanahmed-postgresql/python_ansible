import json
import subprocess

# Read config.json
with open('config.json') as config_file:
    config_data = json.load(config_file)

# Extract required values
ansible_host = config_data['ansible_host']
ansible_connection = config_data['ansible_connection']
ansible_user = config_data['ansible_user']
ansible_become_pass = config_data['ansible_become_pass']

# Execute Ansible playbook
command = [
    'ansible-playbook',
    '-i', ansible_host + ',',
    '-e', f'ansible_connection={ansible_connection}',
    '-e', f'ansible_user={ansible_user}',
    '-e', f'ansible_become_pass={ansible_become_pass}',
    'playbook.yml','-vvv'
]

subprocess.run(command)

