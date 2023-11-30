# Directory Contents
- ``labsystems.yml``: Inventory file. Specifies target machine and variables.
- ``roleserver.yml``: Ansible Playbook
- ``passwords``: Encrypted password file
- ``passwords.swp``: swp file for the ``passwords`` file.
- ``roles`` directory: Contains the ``conntest`` and ``webserver`` roles referenced in the ``roleserver.yml`` playbook. ``conntest`` is a connection test and ``webserver`` sets up the infrastructure.
- ``serverplay.yml``: Test Playbook

# Deployment (in 'ansible' directory):
Vault Pass: vaultpass

```bash
$ ansible-playbook -i labsystems.yml --ask-vault-pass roleserver.yml
```

