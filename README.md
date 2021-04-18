# dnac_playground
Cisco DNA Center Playground

Hi folks,

this is my Cisco DNA Center playground.

# dnacli.py

A script to interact with DNA center from CLI, written in Python.

```
INFO: Showing help with the command 'dnacli.py -- --help'.

NAME
    dnacli.py

SYNOPSIS
    dnacli.py COMMAND

COMMANDS
    COMMAND is one of the following:

     get_config

     get_device_list

     get_interfaces

     run_cmd


```

Example run_cmd:
```
python dnacli.py run_cmd --device_name=cat_9k_1 --command="show ver | inc RELEASE" --wait=10
Task 20373d3c-fbcb-4aeb-a8b3-5ed024459ae2 created.
Wait for response ... break in 10 seconds or CTRL-C to abort.
SUCCESS:
-----------------------------------------------------------------------------------------------
Command: show ver | inc RELEASE
show ver | inc RELEASE
Cisco IOS Software [Amsterdam], Catalyst L3 Switch Software (CAT9K_IOSXE), Version 17.3.1, RELEASE SOFTWARE (fc5)
BOOTLDR: System Bootstrap, Version 17.3.1r[FC2], RELEASE SOFTWARE (P)
cat_9k_1#

```

Example trace_path:
```
python dnacli.py trace_path --srcip=10.10.22.98 --destip=10.10.22.114
Wait for response ... break in 20 seconds or CTRL-C to abort.
Source:                       10.10.22.98
Destination:                  10.10.22.114
Path:
================================================================================
type                          wired
ip                            10.10.22.98
linkInformationSource         Wired
--------------------------------------------------------------------------------
name                          cat_9k_1
type                          Switches and Hubs
ip                            10.10.22.66
ingressInterface              {'id': '4ec5db92-10b3-442e-b302-c5a489b786d8', 'name': 'TenGigabitEthernet1/0/1', 'vrfName': 'global', 'usedVlan': '1'}
                              [{'id': '89d6aad4-5a83-4b00-ad0e-340b85477de8', 'name': 'Vlan1', 'vrfName': 'global', 'usedVlan': '1'}]
egressInterface               {'id': '56d3e822-cbbd-40d9-9141-19644e6cc6ff', 'name': 'TenGigabitEthernet1/1/1', 'vrfName': 'global', 'usedVlan': 'NA'}
role                          ACCESS
linkInformationSource         OSPF
--------------------------------------------------------------------------------
name                          cs3850.abc.inc
type                          Switches and Hubs
ip                            10.10.22.73
ingressInterface              {'id': 'a249983e-0abe-46d8-a04b-78c2bc140082', 'name': 'TenGigabitEthernet1/1/2', 'vrfName': 'global', 'usedVlan': 'NA'}
egressInterface               {'id': 'f50ef49a-d916-47c2-94d6-e4fb16f25817', 'name': 'TenGigabitEthernet1/1/3', 'vrfName': 'global', 'usedVlan': 'NA'}
role                          DISTRIBUTION
linkInformationSource         OSPF
--------------------------------------------------------------------------------
name                          cat_9k_2
type                          Switches and Hubs
ip                            10.10.22.70
ingressInterface              {'id': '5f00153e-9da6-4bf4-bd23-b6296e51a572', 'name': 'TenGigabitEthernet1/1/1', 'vrfName': 'global', 'usedVlan': 'NA'}
egressInterface               {'id': 'cd34d7ed-5938-4828-a449-11ac4ad0f4ed', 'name': 'TenGigabitEthernet1/0/24', 'vrfName': 'global', 'usedVlan': '1'}
                              [{'id': '43a3384d-2bae-4b1a-be70-317c77ee9cd3', 'name': 'Vlan1', 'vrfName': 'global', 'usedVlan': '1'}]
role                          ACCESS
linkInformationSource         Switched
--------------------------------------------------------------------------------
type                          wired
ip                            10.10.22.114
--------------------------------------------------------------------------------


```
