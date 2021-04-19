# dnac_playground
Cisco DNA Center Playground

Hi folks,

this is my Cisco DNA Center playground.

# dnacli.py

A script to interact with DNA center from CLI, written in Python.

```
python dnacli.py --help
INFO: Showing help with the command 'dnacli.py -- --help'.

NAME
    dnacli.py

SYNOPSIS
    dnacli.py COMMAND

COMMANDS
    COMMAND is one of the following:

     backup
       Create backup of given device.

     client_detail
       Get client details to given mac address.

     get_device_list
       Get device list.

     get_interfaces
       Get interfaces of given device.

     run_cmd
       Execute command on device.

     trace_path
       Trace path between 2 ip addresses.

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
ingressInterface              name: TenGigabitEthernet1/0/1 vrfName: global usedVlan: 1
                              name: Vlan1 vrfName: global usedVlan: 1
egressInterface               name: TenGigabitEthernet1/1/1 vrfName: global usedVlan: NA
role                          ACCESS
linkInformationSource         OSPF
--------------------------------------------------------------------------------
name                          cs3850.abc.inc
type                          Switches and Hubs
ip                            10.10.22.73
ingressInterface              name: TenGigabitEthernet1/1/2 vrfName: global usedVlan: NA
egressInterface               name: TenGigabitEthernet1/1/3 vrfName: global usedVlan: NA
role                          DISTRIBUTION
linkInformationSource         OSPF
--------------------------------------------------------------------------------
name                          cat_9k_2
type                          Switches and Hubs
ip                            10.10.22.70
ingressInterface              name: TenGigabitEthernet1/1/1 vrfName: global usedVlan: NA
egressInterface               name: TenGigabitEthernet1/0/24 vrfName: global usedVlan: 1
                              name: Vlan1 vrfName: global usedVlan: 1
role                          ACCESS
linkInformationSource         Switched
--------------------------------------------------------------------------------
type                          wired
ip                            10.10.22.114
--------------------------------------------------------------------------------


```
