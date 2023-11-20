# The following are the steps needed to set up the webserver. Commands must be run with sudo
Look at 5:00 in "W11 L6 - Deploying a Webserver with Ansible"
1. update package repo
sudo apt update

2. install python3
sudo apt install python3

3. install php-cgi
sudo apt install php-cgi

4. copy 'code' folder over to target
dest: /etc/crazycalculators/code

5. Set server.py to run as a service on starup (systemd)

6. execute code/src/server.py
python3 server.py 80 0.0.0.0

# To deploy(in 'ansible' dir):
Vault Pass: vaultpass
$ ansible-playbook -i labsystems.yml --ask-vault-pass roleserver.yml
