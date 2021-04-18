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

Example:
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
