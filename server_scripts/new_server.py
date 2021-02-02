from fabric import Connection, Config
from server_util import *
import yaml
import logging
import sys

def setup_server():    
    config = get_config()
    commands = []

    # Setup sudo user
    sudo_user_config = config[SUDO_USER_FIELD]
    username = sudo_user_config[USERNAME_FIELD]
    commands += sudo_user_commands(username, sudo_user_config[PASSWORD_FIELD])

    # Configure firewall
    ufw_config = config[UFW_FIELD]
    commands += ufw_default_commands(ufw_config[INCOMING_UFW_FIELD], ufw_config[OUTGOING_UFW_FIELD])

    # Update packages
    commands += packages_update_commands()

    # Install starters
    starters = config.get(STARTERS_FIELD)
    if (starters != None):
        for start_commands in list(map(lambda name: starter_commands(name, username), starters)):
            commands += start_commands

    # Run commands
    ssh_config = config[SSH_FIELD]
    run_commands(commands, config[HOSTNAME_FIELD], ssh_config[KEY_LOCATION_FIELD], ssh_config[KEY_PASSPHRASE_FIELD])

def get_config():
    with open("config.yml", "r") as stream:
        return yaml.safe_load(stream)

def configure_logging():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.getLogger('paramiko').setLevel(logging.INFO)

def create_ssh_client(hostname, ssh_key_location):
    if (ssh_key_location.endswith('ppk')):
        raise ValueError('.ppk ssh keys are not supported. Please convert to OpenSSH.')
    client = Connection(hostname,  user='root', connect_kwargs={'key_filename': ssh_key_location})
    return client

if __name__ == '__main__':
    setup_server()