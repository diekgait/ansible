# Ansible playbooks for use with Netbox

This repository cointains a couple Ansbile playbooks to use in combination with Netbox.

## Inventory

The inventory folder contains exsample playbooks to inventory networkhardware and fill Netbox with te aquired data.

## config_gen

The config_gen folder contains a working example that:
- Generates a Cisco IOS config based on a template and dynamic data from netbox
- Installs this config on an IOS device.