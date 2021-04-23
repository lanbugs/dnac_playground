import requests
import json
from pprint import pprint
requests.packages.urllib3.disable_warnings()


USERNAME = "admin"
PASSWORD = "1234QWer"
URL = "https://192.168.10.1/"

# 1. Authentication
payload = {
	'aaaUser': {
		'attributes': {
			'name': USERNAME,
            'pwd': PASSWORD
            }
        }
}

auth = requests.post(f'{URL}api/aaaLogin.json', data=json.dumps(payload), verify=False)
COOKIES = auth.cookies

# 2. task
"""
method: POST
url: https://192.168.10.1/api/node/mo/uni/infra/hpaths-101_eth1_14.json
payload"{
    \"infraHPathS\":{
        \"attributes\":{
            \"rn\":\"hpaths-101_eth1_14\",
            \"dn\":\"uni/infra/hpaths-101_eth1_14\",
            \"descr\":\"test\",
            \"name\":\"101_eth1_14\"},
        \"children\":[
            {\"infraRsHPathAtt\":{
                \"attributes\":{
                    \"dn\":\"uni/infra/hpaths-101_eth1_14/rsHPathAtt-[topology/pod-1/paths-101/pathep-[eth1/14]]\",
                    \"tDn\":\"topology/pod-1/paths-101/pathep-[eth1/14]\"
                    }
                }
            }
        ]
    }
}"
response: {"totalCount":"0","imdata":[]}
"""
POD_ID = '1'
LEAF_ID = '101'
# Example: Eth 1/14 => MOD_ID = 1 PORT_ID=14
MOD_ID = '1'
PORT_ID = '14'
DESCR = 'TEST INTERFACE'

payload_task = {
    'infraHPathS': {
        'attributes': {
            'dn': f'uni/infra/hpaths-{LEAF_ID}_eth{MOD_ID}_{PORT_ID}',
            'name': f'{LEAF_ID}_eth{MOD_ID}_{PORT_ID}',
            'descr': DESCR,
            'rn': f'hpaths-{LEAF_ID}_eth{MOD_ID}_{PORT_ID}'
        },
        'children': [
            {'infraRsHPathAtt': {
                'attributes': {
                    'dn': f'uni/infra/hpaths-{LEAF_ID}_eth{MOD_ID}_{PORT_ID}/rsHPathAtt-[topology/pod-{POD_ID}/paths-{LEAF_ID}/pathep-[eth{MOD_ID}/{PORT_ID}]]',
                    'tDn': f'topology/pod-{POD_ID}/paths-{LEAF_ID}/pathep-[eth{MOD_ID}/{PORT_ID}]'
                    }
                }
            }
        ]
    }
}

result = requests.post(f'{URL}api/node/mo/uni/infra/hpaths-{LEAF_ID}_eth1_14.json', data=json.dumps(payload_task), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result.status_code))
pprint(result.content)
