#!/usr/bin/python

# Copyright 2015 Patrick Ogenstad <patrick@ogenstad.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

DOCUMENTATION = '''
---

module: cisco_asa_network_object
author: Patrick Ogenstad (@networklore)
version: 1.0
short_description: Creates deletes or edits network objects.
description:
    - Configures network objects
requirements:
    - rasa
options:
    category:
        description:
            - The type of object you are creating. Use slash notation for subnets, i.e. 192.168.0.0/24. Use - for ranges, i.e. 192.168.0.1-192.168.0.10. 
        choices: [ 'ipv4_address', 'ipv6_address', 'ipv4_subnet', 'ipv6_subnet', 'ipv4_range', 'ipv6_range', 'ipv4_fqdn', 'ipv6_fqdn' ]
        required: false
    description:
        description:
            - Description of the object
        required: false
    host:
        description:
            - Typically set to {{ inventory_hostname }}
        required: true
    name:
        description:
            - Name of the network object
        required: true
    password:
        description:
            - Password for the device
        required: true
    state:
        description:
            - State of the object
        choices: [ 'present', 'absent' ]
        required: true
    username:
        description:
            - Username for device
        required: true
    validate_certs:
        description:
            - If no, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.
        choices: [ 'no', 'yes']
        default: 'yes'
        required: false
    value:
        description:
            - The data to enter into the network object
        required: false

'''

EXAMPLES = '''

# Create a network object for a web server
- cisco_asa_network_object:
    host={{ inventory_hostname }}
    username=api_user
    password=APIpass123
    name=tsrv-web-1
    state=present
    category=ipv4_address
    description='Test web server'
    value='10.12.30.10'
    validate_certs=no

# Remove test webserver
- cisco_asa_network_object:
    host={{ inventory_hostname }}
    username=api_user
    password=APIpass123
    name=tsrv-web-2
    state=absent
    validate_certs=no
'''

import sys
from ansible.module_utils.basic import *
from collections import defaultdict

try:
    from rasa import ASA
    has_rasa = True
except:
    has_rasa = False

object_kind = {
    'ipv4_address': 'IPv4Address',
    'ipv6_address': 'IPv6Address',
    'ipv4_subnet': 'IPv4Network',
    'ipv6_subnet': 'IPv6Network',
    'ipv4_range': 'IPv4Range',
    'ipv6_range': 'IPv6Range',
    'ipv4_fqdn': 'IPv4FQDN',
    'ipv6_fqdn': 'IPv6FQDN'
}

def create_object(dev, module, desired_data):
    try:
        result = dev.create_networkobject(desired_data)
    except:
        err = sys.exc_info()[0]
        module.fail_json(msg='Unable to connect to device: %s' % err)

    if result.status_code == 201:
        return_status = True
    else:
        module.fail_json(msg='Unable to create object - %s' % result.status_code)

    return return_status

def delete_object(dev, module, name):
    try:
        result = dev.delete_networkobject(name)
    except:
        err = sys.exc_info()[0]
        module.fail_json(msg='Unable to connect to device: %s' % err)

    if result.status_code == 204:
        return_status = True
    else:
        module.fail_json(msg='Unable to delete object - %s' % result.status_code)

    return return_status

def main():
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(required=True),
            username=dict(required=True),
            password=dict(required=True),
            name=dict(required=True),
            description=dict(required=False),
            state=dict(required=True, choices=['absent', 'present']),
            category=dict(required=False, choices=[ 'ipv4_address', 'ipv6_address', 'ipv4_subnet', 'ipv6_subnet', 'ipv4_range', 'ipv6_range', 'ipv4_fqdn', 'ipv6_fqdn' ]),
            validate_certs=dict(required=False, choices=['no', 'yes'], default='yes'),
            value=dict(required=False)),
            required_together = ( ['category','value'],),
        supports_check_mode=False)

    m_args = module.params

    if not has_rasa:
        module.fail_json(msg='Missing required rasa module (check docs)')

    if m_args['state'] == "present":
        if m_args['category'] == False:
            module.fail_json(msg='Category not defined')
    if m_args['validate_certs'] == 'yes':
        validate_certs = True
    else:
        validate_certs = False

    dev = ASA(
        device=m_args['host'],
        username=m_args['username'],
        password=m_args['password'],
        verify_cert=validate_certs
    )

    desired_data = {}
    desired_data['name'] = m_args['name']
    desired_data['objectId'] = m_args['name']
    desired_data['kind'] = 'object#NetworkObj'
    if m_args['category']:
        kind = object_kind[m_args['category']]
        desired_data['host'] = {
            'kind': kind,
            'value': m_args['value']
        }

    if m_args['description']:
        desired_data['description'] = m_args['description']

    try:
        data = dev.get_networkobject(m_args['name'])
    except:
        err = sys.exc_info()[0]
        module.fail_json(msg='Unable to connect to device: %s' % err)

    if data.status_code == 200:
        if m_args['state'] == 'absent':
            changed_status = delete_object(dev, module, m_args['name'])
        elif m_args['state'] == 'present':

            matched = match_objects(data.json(), desired_data, module)
            if matched:
                changed_status = False
            else:
                changed_status = update_object(dev, module, desired_data)

    elif data.status_code == 401:
        module.fail_json(msg='Authentication error')

    elif data.status_code == 404:
        if m_args['state'] == 'absent':
            changed_status = False
        elif m_args['state'] == 'present':
            changed_status = create_object(dev, module, desired_data)
    else:
        module.fail_json(msg="Unsupported return code %s" % data.status_code)

    return_msg = {}
    return_msg['changed'] = changed_status

    module.exit_json(**return_msg)
    
def match_objects(current_data, desired_data, module):
    has_current_desc = False
    has_desired_desc = False

    if 'description' in current_data.keys():
        has_current_desc = True
        
    if 'description' in desired_data.keys():
        has_desired_desc = True

    if has_current_desc == has_desired_desc:
        if has_desired_desc == True:
            if current_data['description'] != desired_data['description']:
                return False
    else:
        return False

    if current_data['host'] != desired_data['host']:
        return False
    return True


def update_object(dev, module, desired_data):
    try:
        result = dev.update_networkobject(desired_data['name'], desired_data)
    except:
        err = sys.exc_info()[0]
        module.fail_json(msg='Unable to connect to device: %s' % err)

    if result.status_code == 204:
        return_status = { 'changed': True }
    else:
        module.fail_json(msg='Unable to update object code: - %s' % result.status_code)

    return return_status



main()

