# Server Scripts

These scripts are designed for configuring new servers.

Currently the scripts have been tested for Ubuntu 20.04.
If I end up using other distributions, I will update the script to support them.

## Library requirements

```sh
pip install fabric
pip install pyyaml 
```

## config.yml

All scripts use a file named ```config.yml``` to guide their behaviour. This file should be placed in the same directory as the scripts.

The required fields for each script are given in their respective documentation below.

```yml
# Hostname of the server to be configured
hostname: '192.168.0.256'
# The path to your public ssh key, used by root
ssh:
    key_location: '/keys/x.txt'
    key_passphrase: 'notpassword123'
# The username and password for the sudo user
sudo:
    username: 'monty'
    password: 'python'
# Uncomplicated Firewall default settings for incoming/outgoing connections
ufw:
  incoming: 'deny'
  outgoing: 'allow'
# A list of starters to install, see add_starter.py below
starters:
    - node
```

## new_server.py

| Required Fields | |
| --- | --- |
| hostname |  |
| ssh.key_location | ssh.key_passphrase also required if key has one |
| sudo.username, sudo.password |  |
| ufw.incoming, ufw.outgoing |  |

Configures a server for first time setup. This script will:

- Set up a sudo user
- Configure UFW
- Upgrade the package manager
- Configure any specified starters

The configuration is specified in config.yml:

## add_starter.py

| Required Fields | |
| --- | --- |
| hostname |  |
| ssh.key_location | ssh.key_passphrase also required if key has one |
| sudo.username | Required for starters that substitute the sudo username into their commands |

Starters are sets of packages and commands that configure the server for a particular task. Starters are configured using YAML files in the [/starters/](/starters/) folder.

```yml
packages:
    - nodejs
    - python3.9
commands:
    - echo Hello, world!
```

The packages will be installed using ```apt-get```, and then the commands will be run to set up the starter on the host.

The name of the starter is passed to the script when it is run. The name must match the file name without it's .yml extension:

```python add_starter.py <starter_name>```
