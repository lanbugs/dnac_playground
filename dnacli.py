#!/usr/bin/env python3

import fire
import requests
from requests.auth import HTTPBasicAuth
import json
import time

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

    def get_config(self):
        print(self.__DNAC_URL, self.__DNAC_USER, self.__DNAC_PASSWORD)

    def __get_device_list_json(self):
        url = self.__url('api/v1/network-device')
        hdr = {'x-auth-token': self.__token, 'content-type': 'application/json'}
        resp = requests.get(url, headers=hdr)
        device_json = resp.json()
        return device_json

    def get_device_list(self):
        device_list = self.__get_device_list_json()

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
        # determine deviceId
        device_list = self.__get_device_list_json()

        for device in device_list['response']:
            if device_name == device['hostname']:
                device_id = device['id']

        url = self.__url('api/v1/interface')
        hdr = {'x-auth-token': self.__token, 'content-type': 'application/json'}
        querystring = { "deviceId": device_id}
        resp = requests.get(url, headers=hdr, params=querystring)
        interface_info_json = resp.json()

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
        # determine deviceId
        device_list = self.__get_device_list_json()

        for device in device_list['response']:
            if device_name == device['hostname']:
                device_id = device['id']

        url = self.__url('api/v1/network-device-poller/cli/read-request')
        hdr = {'x-auth-token': self.__token, 'content-type': 'application/json'}
        params = {'deviceId': device_id}

        payload = {
            "name" : command,
            "commands" : [ command ],
            "deviceUuids" : [ device_id ]
        }

        payload_json = json.dumps(payload)

        resp = requests.post(url, headers=hdr, params=params, data=payload_json)

        answer = resp.json()

        print("Task %s created." % answer['response']['taskId'])

        task_url = self.__url('api/v1/task/%s' % answer['response']['taskId'])

        while 1:
            task_resp = requests.get(task_url, headers=hdr)

            if task_resp.status_code == 200:
                answer_task = task_resp.json()

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

        url_file = self.__url('api/v1/file/%s' % fileId)
        resp_file = requests.get(url_file, headers=hdr)

        results = resp_file.json()

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


if __name__ == '__main__':
    dna = DNACcli(DNAC_URL, DNAC_USER, DNAC_PASSWORD)
    fire.Fire(dna)
