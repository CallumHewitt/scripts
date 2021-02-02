from server_util import *
from sys import argv 

def add_starter(starter_name):    
    config = get_config()
    commands = starter_commands(starter_name, config[SUDO_USER_FIELD][USERNAME_FIELD])
    ssh_config = config[SSH_FIELD]
    run_commands(commands, config[HOSTNAME_FIELD], ssh_config[KEY_LOCATION_FIELD], ssh_config[KEY_PASSPHRASE_FIELD])

if __name__ == '__main__':
    add_starter(argv[1])