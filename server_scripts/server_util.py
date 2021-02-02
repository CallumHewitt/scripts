import yaml
import logging
import sys
from fabric import Connection

HOSTNAME_FIELD = 'hostname'
SSH_FIELD = 'ssh'
KEY_LOCATION_FIELD = 'key_location'
KEY_PASSPHRASE_FIELD = 'key_passphrase'

SUDO_USER_FIELD = "sudo"
USERNAME_FIELD = 'username'
PASSWORD_FIELD = 'password'

UFW_FIELD = 'ufw'
INCOMING_UFW_FIELD = 'incoming'
OUTGOING_UFW_FIELD = 'outgoing'

STARTERS_FIELD = 'starters'

PACKAGES_FIELD = 'packages'
COMMANDS_FIELD = 'commands'

def sudo_user_commands(username, password):
    return [
        f'echo "{username}:{password}::::/home/{username}:/bin/bash" | newusers',
        f'rsync --archive --chown={username}:{username} ~/.ssh /home/{username}',
        f'usermod -aG sudo {username}' 
    ]

def ufw_default_commands(incoming_rule, outgoing_rule):
    if not (incoming_rule == 'allow' or incoming_rule == 'deny'):
        raise ValueError(f'incoming_rule was {incoming_rule}. It must be \'allow\' or \'deny\'')
    if not (outgoing_rule == 'allow' or outgoing_rule == 'deny'):
        raise ValueError(f'outgoing_rule was {outgoing_rule}. It must be \'allow\' or \'deny\'')
    return [
        f'ufw default {incoming_rule} incoming',
        f'ufw default {outgoing_rule} outgoing',
        'ufw allow ssh',
        'yes | ufw enable'
    ]

def packages_update_commands():
    return [
        'apt-get update',
        'apt-get --yes -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confnew" upgrade',
        'apt-get --yes -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confnew" dist-upgrade',
        'apt-get --yes autoremove',
        'apt-get --yes autoclean'
    ]

def starter_commands(starter_name, sudo_user):
    starter_config = get_starter_config(starter_name)
    print(starter_config)
    commands = []
    packages = starter_config[PACKAGES_FIELD]
    if (packages != None):
        commands += list(map(lambda pkg: f'apt-get install -y {pkg}', starter_config[PACKAGES_FIELD]))
    if (commands != None):
        raw_commands = starter_config[COMMANDS_FIELD]
        if (sudo_user != None):
            commands += list(map(lambda command: command.replace('$SUDO_USER', sudo_user), raw_commands))
        else:
            commands += raw_commands
    return commands

def get_starter_config(name):
    with open(f'starters/{name}.yml', 'r') as stream:
        return yaml.safe_load(stream)

def run_commands(commands, hostname, ssh_key_location, ssh_key_passphrase):
    configure_logging()
    client = create_ssh_client(hostname, ssh_key_location, ssh_key_passphrase)
    for command in commands:
        logging.info(f'Running: {command}')
        client.run(command)

def get_config():
    with open("config.yml", "r") as stream:
        return yaml.safe_load(stream)

def configure_logging():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.getLogger('paramiko').setLevel(logging.INFO)

def create_ssh_client(hostname, ssh_key_location, ssh_key_passphrase):
    if (ssh_key_location.endswith('ppk')):
        raise ValueError('.ppk ssh keys are not supported. Please convert to OpenSSH.')
    connect_args = {'key_filename': ssh_key_location}    
    if (ssh_key_passphrase):
        connect_args['passphrase'] = ssh_key_passphrase
    client = Connection(hostname, user='root', connect_kwargs=connect_args)
    return client