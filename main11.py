import json
import subprocess
from cryptography.fernet import Fernet

# Function to encrypt the value
def encrypt_value(fernet, value):
    return fernet.encrypt(value.encode()).decode()

# Function to decrypt the value
def decrypt_value(fernet, encrypted_value):
    return fernet.decrypt(encrypted_value.encode()).decode()

# Read the config.json file
with open('config.json') as config_file:
    config_data = json.load(config_file)

# Generate a new encryption key
encryption_key = Fernet.generate_key()
fernet = Fernet(encryption_key)

# Encrypt the sensitive values in the config file
for section in ['common_variables', 'primary_variables']:
    if isinstance(config_data[section], dict):
        for key, value in config_data[section].items():
            config_data[section][key] = encrypt_value(fernet, value)

# Save the encrypted values back to the config file
with open('config.json', 'w') as config_file:
    json.dump(config_data, config_file, indent=4)

# Save the encryption key to a file
with open('encryption_key.txt', 'wb') as key_file:
    key_file.write(encryption_key)

# Read the encryption key from the file
with open('encryption_key.txt', 'rb') as key_file:
    encryption_key = key_file.read()

# Initialize the Fernet object with the encryption key
fernet = Fernet(encryption_key)

# Decrypt the sensitive values for runtime use
decrypted_config_data = {}
for section in ['common_variables', 'primary_variables']:
    if isinstance(config_data[section], dict):
        decrypted_config_data[section] = {
            key: decrypt_value(fernet, encrypted_value)
            for key, encrypted_value in config_data[section].items()
        }

# Extract required values
common_variables = decrypted_config_data['common_variables']
primary_variables = decrypted_config_data['primary_variables']

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
    'playbook.yml'
]

# Extend command with extra variables
for key, value in extra_vars.items():
    command.extend(['-e', f'{key}={value}'])

subprocess.run(command)

