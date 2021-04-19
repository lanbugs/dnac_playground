#!/usr/bin/env python3

import fire
import loguru
import requests
from requests.auth import HTTPBasicAuth
import json
import time
from loguru import logger

########################################################################################################################
# dnacli.py
# More details on https://lanbugs.de or https://github.com/lanbugs/dnac_playground
# Required modules:
# fire, requests

###############################################################################
# SETTINGS
DNAC_URL = "https://sandboxdnac.cisco.com/"
DNAC_USER = "devnetuser"
DNAC_PASSWORD = "Cisco123!"

@logger.catch
class DNACcli:

    def __init__(self, DNAC_URL, DNAC_USER, DNAC_PASSWORD):
        self.__DNAC_URL = DNAC_URL
        self.__DNAC_USER = DNAC_USER
        self.__DNAC_PASSWORD = DNAC_PASSWORD

        self.__get_auth_token()

    def __url(self, surl):
        return DNAC_URL+surl

    def __get_auth_token(self):
        url = self.__url('dna/system/api/v1/auth/token')
        resp = requests.post(url, auth=HTTPBasicAuth(self.__DNAC_USER, self.__DNAC_PASSWORD))
        self.__token = resp.json()['Token']

    def __get_config(self):
        print(self.__DNAC_URL, self.__DNAC_USER, self.__DNAC_PASSWORD)

    def __get(self, surl, params=None):
        url = self.__url(surl)
        hdr = {'x-auth-token': self.__token, 'content-type': 'application/json'}
        resp = requests.get(url, headers=hdr, params=params)
        return resp.json()

    def __post(self, surl, params=None, payload={}):
        url = self.__url(surl)
        hdr = {'x-auth-token': self.__token, 'content-type': 'application/json'}
        payload_json = json.dumps(payload)
        resp = requests.post(url, headers=hdr, params=params, data=payload_json)
        return resp.json()

    def __get_device_list_json(self):
        url = self.__url('api/v1/network-device')
        hdr = {'x-auth-token': self.__token, 'content-type': 'application/json'}
        resp = requests.get(url, headers=hdr, params=None)
        device_json = resp.json()
        return device_json

    def __dict_to_str(self, i_dict):
        buffer = ""
        if isinstance(i_dict, list):
            for item in i_dict:
                for key, value in item.items():
                    if key != "id":
                        buffer += "%s: %s " % (str(key), str(value))
        else:
            for key, value in i_dict.items():
                if key != "id":
                    buffer += "%s: %s " % (str(key), str(value))
        return buffer

    def get_device_list(self):
        """Get device list."""
        device_list = self.__get('api/v1/network-device')

        print("{0:42}{1:17}{2:12}{3:18}{4:12}{5:16}{6:15}".
              format("hostname", "mgmt IP", "serial", "platformId", "SW Version", "role", "Uptime"))

        for device in device_list['response']:
            uptime = "N/A" if device['upTime'] is None else device['upTime']
            if device['serialNumber'] is not None and "," in device['serialNumber']:
                serialPlatformList = zip(device['serialNumber'].split(","), device['platformId'].split(","))
            else:
                serialPlatformList = [(device['serialNumber'], device['platformId'])]
            for (serialNumber, platformId) in serialPlatformList:
                print("{0:42}{1:17}{2:12}{3:18}{4:12}{5:16}{6:15}".
                      format(device['hostname'],
                             device['managementIpAddress'],
                             serialNumber,
                             platformId,
                             device['softwareVersion'],
                             device['role'], uptime))

    def get_interfaces(self, device_name):
        """Get interfaces of given device."""
        # determine deviceId
        device_list = self.__get('api/v1/network-device')

        for device in device_list['response']:
            if device_name == device['hostname']:
                device_id = device['id']

        params = {"deviceId": device_id}
        interface_info_json = self.__get('api/v1/interface', params=params)

        print("{0:42}{1:20}{2:14}{3:18}{4:17}{5:10}{6:15}".
              format("portName", "vlanId", "portMode", "portType", "duplex", "status", "lastUpdated"))
        for int in interface_info_json['response']:
            print("{0:42}{1:20}{2:14}{3:18}{4:17}{5:10}{6:15}".
                  format(str(int['portName']),
                         str(int['vlanId']),
                         str(int['portMode']),
                         str(int['portType']),
                         str(int['duplex']),
                         str(int['status']),
                         str(int['lastUpdated'])))

    def run_cmd(self, device_name, command, wait=20):
        """Execute command on device."""
        # determine deviceId
        device_list = self.__get('api/v1/network-device')

        for device in device_list['response']:
            if device_name == device['hostname']:
                device_id = device['id']

        params = {'deviceId': device_id}
        payload = {
            "name" : command,
            "commands" : [ command ],
            "deviceUuids" : [ device_id ]
        }

        answer = self.__post('api/v1/network-device-poller/cli/read-request', params=params, payload=payload)

        print("Task %s created." % answer['response']['taskId'])

        while 1:
            answer_task = self.__get('api/v1/task/%s' % answer['response']['taskId'])

            if "fileId" in answer_task['response']['progress']:
               break

            time.sleep(1)
            print("Wait for response ... break in %s seconds or CTRL-C to abort." % wait)
            wait -= 1

            if wait == 0:
                break

        progress_json = answer_task['response']['progress']
        progress = json.loads(progress_json)
        fileId = progress['fileId']

        results = self.__get('api/v1/file/%s' % fileId)

        for result in results:
            if len(result['commandResponses']['SUCCESS']) > 0:
                print("SUCCESS:")
                print("-----------------------------------------------------------------------------------------------")
                for key, value in result['commandResponses']['SUCCESS'].items():
                    print("Command: %s " % key)
                    print(value)
            elif len(result['commandResponses']['FAILURE']) > 0:
                print("FAILURE:")
                print("-----------------------------------------------------------------------------------------------")
                for key, value in result['commandResponses']['FAILURE'].items():
                    print("Command: %s " % key)
                    print(value)
            elif len(result['commandResponses']['BLACKLISTED']) > 0:
                print("BLACKLISTED:")
                print("-----------------------------------------------------------------------------------------------")
                for key, value in result['commandResponses']['BLACKLISTED'].items():
                    print("Command: %s " % key)
                    print(value)

    def trace_path(self, srcip, destip, wait=20):
        """Trace path between 2 ip addresses."""

        payload = {
            "sourceIP": srcip,
            "destIP": destip
        }

        answer = self.__post('dna/intent/api/v1/flow-analysis', payload=payload)

        flowAnalysisId = answer['response']['flowAnalysisId']

        while 1:
            flow_answer = self.__get('dna/intent/api/v1/flow-analysis/%s' % flowAnalysisId)

            if flow_answer['response']['request']['status'] == "COMPLETED":
                break

            time.sleep(1)
            print("Wait for response ... break in %s seconds or CTRL-C to abort." % wait)
            wait -= 1

            if wait == 0:
                break

        print("{0:30}{1:50}".format("Source:", srcip))
        print("{0:30}{1:50}".format("Destination:", destip))
        print("Path:")
        print("="*80)
        for element in flow_answer['response']['networkElementsInfo']:

            for key, value in element.items():
                if key != "id":
                    if isinstance(value, dict):
                        c = 0
                        for k, v in value.items():
                            if c == 0:
                                print("{0:30}{1:50}".format(key, str(self.__dict_to_str(v))))
                                c += 1
                            else:
                                print("{0:30}{1:50}".format("", str(self.__dict_to_str(v))))
                    else:
                        print("{0:30}{1:50}".format(key, str(value)))

            print("-" * 80)

    def backup(self, device_name, wait=20):
        """Create backup of given device."""
        # determine deviceId
        device_list = self.__get('api/v1/network-device')

        for device in device_list['response']:
            if device_name == device['hostname']:
                device_id = device['id']

        params = {'deviceId': device_id}
        payload = {
            "name" : "show run",
            "commands" : ["show run"],
            "deviceUuids" : [device_id]
        }

        answer = self.__post('api/v1/network-device-poller/cli/read-request', params=params, payload=payload)

        print("Task %s created." % answer['response']['taskId'])

        while 1:
            answer_task = self.__get('api/v1/task/%s' % answer['response']['taskId'])
            if "fileId" in answer_task['response']['progress']:
               break
            time.sleep(1)
            print("Wait for response ... break in %s seconds or CTRL-C to abort." % wait)
            wait -= 1
            if wait == 0:
                break

        progress_json = answer_task['response']['progress']
        progress = json.loads(progress_json)
        fileId = progress['fileId']

        results = self.__get('api/v1/file/%s' % fileId)

        for result in results:
            if len(result['commandResponses']['SUCCESS']) > 0:
                print("SUCCESS:")
                print("-----------------------------------------------------------------------------------------------")
                for key, value in result['commandResponses']['SUCCESS'].items():
                    print("Command: %s " % key)
                    print("Stored to: %s.txt" % device_name)
                    with open("%s.txt" % device_name, "w") as f:
                        f.write(value)
            else:
                print ("Something went wrong")

    def client_detail(self, mac):
        """Get client details to given mac address."""
        # DEV
        params = {
            "macAddress": mac
        }

        result = self.__get('dna/intent/api/v1/client-detail', params=params)

        from pprint import pprint
        pprint(result)


if __name__ == '__main__':
    dna = DNACcli(DNAC_URL, DNAC_USER, DNAC_PASSWORD)
    fire.Fire(dna)
