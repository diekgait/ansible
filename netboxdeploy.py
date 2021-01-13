#!/usr/bin/env python

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import sys
import pynetbox
from packaging import version

# NOTE: If anything depends on specific versions of NetBox, can check INTEGRATION_TESTS in env
# os.environ["INTEGRATION_TESTS"]


# Set nb variable to connect to Netbox and use the veriable in future calls
nb_host = os.getenv("NETBOX_HOST", "https://vps01.lansink.it")
nb_token = os.getenv("NETBOX_TOKEN", "4e78012ed28ded8da1697f866c372838e29983bd")
nb = pynetbox.api(nb_host, nb_token)
nb_version = version.parse(nb.version)

ERRORS = False


def make_netbox_calls(endpoint, payload):
    """Make the necessary calls to create endpoints, and pass any errors.

    Args:
        endpoint (obj): pynetbox endpoint object.
        payload (list): List of endpoint objects.
    """
    try:
        created = endpoint.create(payload)
    except pynetbox.RequestError as e:
        print(e.error)
        ERRORS = True
        return

    return created


# Create tags used in future tests
if nb_version >= version.parse("2.9"):
    create_tags = nb.extras.tags.create(
        [
            {"name": "First", "slug": "first"},
            {"name": "Second", "slug": "second"},
            {"name": "Third", "slug": "third"},
            {"name": "Schnozzberry", "slug": "schnozzberry"},
            {"name": "Lookup", "slug": "lookup"},
            {"name": "Nolookup", "slug": "nolookup"},
            {"name": "tagA", "slug": "taga"},
            {"name": "tagB", "slug": "tagb"},
            {"name": "tagC", "slug": "tagc"},
            {"name": "Updated", "slug": "updated"},
        ]
    )

# ORDER OF OPERATIONS FOR THE MOST PART
## Create SITES and register variables
sites = [
    {
        "name": "Test Site",
        "slug": "test-site",
    },
]
created_sites = make_netbox_calls(nb.dcim.sites, sites)
### Site variables to be used later on
test_site = nb.dcim.sites.get(slug="test-site")

## Create Manufacturers
manufacturers = [
    {"name": "Cisco", "slug": "cisco"},
]
created_manufacturers = make_netbox_calls(nb.dcim.manufacturers, manufacturers)
### Manufacturer variables to be used later on
cisco_manu = nb.dcim.manufacturers.get(slug="cisco")

## Create Device Types
device_types = [
    {"model": "Cisco CSR1000V", "slug": "cisco-csr1000v", "manufacturer": cisco_manu.id},
    {"model": "IOSv switch", "slug": "iosv-switch", "manufacturer": cisco_manu.id},
    {"model": "IOS XRV router", "slug": "ios-xrv-router", "manufacturer": cisco_manu.id},
    {"model": "Nexus 9000v", "slug": "nexus-9000v", "manufacturer": cisco_manu.id},
]

created_device_types = make_netbox_calls(nb.dcim.device_types, device_types)

### Device type variables to be used later on
cisco_csr1000v = nb.dcim.device_types.get(slug="cisco-csr1000v")
iosv_switch = nb.dcim.device_types.get(slug="iosv-switch")
ios_xrv_router = nb.dcim.device_types.get(slug="ios-xrv-router")
nexus_9000v = nb.dcim.device_types.get(slug="nexus-9000v")

## Create Device Roles
device_roles = [
    {"name": "Core Router", "slug": "core-router", "vm_role": False},
    {"name": "Distributie Router", "slug": "distributie-router", "vm_role": False},
    {"name": "Internet Router", "slug": "internet-router", "vm_role": False},
    {"name": "Edge Switch", "slug": "edge-switch", "vm_role": False},
    {"name": "Distributie Switch", "slug": "distributie-switch", "vm_role": False},
]
created_device_roles = make_netbox_calls(nb.dcim.device_roles, device_roles)
### Device role variables to be used later on
core_router = nb.dcim.device_roles.get(slug="core-router")
core_router = nb.dcim.device_roles.get(slug="core-router")
core_router = nb.dcim.device_roles.get(slug="core-router")
core_router = nb.dcim.device_roles.get(slug="core-router")
core_router = nb.dcim.device_roles.get(slug="core-router")

## Create IP Addresses
ip_addresses = [
    {"address": "10.10.20.181/32"},
    {"address": "10.10.20.172/32"},
    {"address": "10.10.20.173/32"},
    {"address": "10.10.20.174/32"},
    {"address": "10.10.20.175/32"},
    {"address": "10.10.20.176/32"},
    {"address": "10.10.20.177/32"},
    {"address": "10.10.20.178/32"},
]
created_ip_addresses = make_netbox_calls(nb.ipam.ip_addresses, ip_addresses)

## Create Devices
devices = [
    {
        "name": "internet-rtr01",
        "device_type": cisco_csr1000v.id,
        "device_role": internet-router.id,
        "site": test_site.id,
    },
    {
        "name": "edge-sw01",
        "device_type": iosv_switch.id,
        "device_role": edge-switch.id,
        "site": test_site.id,
    },  
	{
        "name": "core-rtr01",
        "device_type": ios-xrv-router.id,
        "device_role": core-router.id,
        "site": test_site.id,
    },
    {
        "name": "core-rtr02",
        "device_type": ios-xrv-router.id,
        "device_role": core-router.id,
        "site": test_site.id,
    },
    {
        "name": "dist-rtr01",
        "device_type": cisco-csr1000v.id,
        "device_role": distributie-router.id,
        "site": test_site.id,
    },  
	{
        "name": "dist-rtr02",
        "device_type": cisco-csr1000v.id,
        "device_role": distributie-router.id,
        "site": test_site.id,
    },	
    {
        "name": "dist-sw01",
        "device_type": nexus-n9000v.id,
        "device_role": distributie-switch.id,
        "site": test_site.id,
    },  
	{
        "name": "dist-sw02",
        "device_type": nexus-n9000v.id,
        "device_role": distributie-switch.id,
        "site": test_site.id,
    },	
]
created_devices = make_netbox_calls(nb.dcim.devices, devices)

if nb_version > version.parse("2.8"):
    temp_ips = []
    for ip in ip_addresses:
        if ip.get("interface"):
            ip["assigned_object_id"] = ip.pop("interface")
            ip["assigned_object_type"] = "dcim.interface"
        temp_ips.append(ip)

if ERRORS:
    sys.exit(
        "Errors have occurred when creating objects, and should have been printed out. Check previous output."
    )