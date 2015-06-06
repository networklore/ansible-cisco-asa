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

module: cisco_asa_ikev1_policy
author: Patrick Ogenstad (@networklore)
version: 0.x
short_description: Creates deletes or edits ikev1 policies.
description:
    - Creates deletes or edits ikev1 policies.
requirements:
    - rasa
options:
    authentication:
        description:
            - Authentication method
        choices: [ 'pre-share', 'rsa-sig' ]
        required: false
    encryption:
        description:
            - Encryption Algorithm
        choices: [ 'des', '3des', 'aes-128', 'aes-192', 'aes-256' ]
        required: false
    hash:
        description:
            - Hash Algorithm
        choices: [ 'md5', 'sha' ]
        required: false
    host:
        description:
            - Typically set to {{ inventory_hostname }}
        required: true
    group:
        description:
            - Diffie-Hellman group
        choices: [ '1', '2', '5' ]
        required: false
    lifetime:
        description:
            - SA Lifetime (seconds)
        choices: [ '120-2147483647' ]
        required: true
    password:
        description:
            - Password for the device
        required: true
    priority:
        description:
            - The priority number of the ikev1 policy. 
        choices: [ '1-65535' ]
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
'''

EXAMPLES = '''

# Create an IKEv1 policy
- cisco_ikev1_policy:
    host={{ inventory_hostname }}
    username=api_user
    password=APIpass123
    state=present
    validate_certs=no
    priority=100
    authentication=pre-share
    encryption=aes-256
    hash=sha
    group=5
    lifetime=28800


# Remove an IKEv1 policy
- cisco_ikev1_policy:
    host={{ inventory_hostname }}
    username=api_user
    password=APIpass123
    policy=12
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

def create_object(dev, module, desired_data):
    try:
        result = dev.create_ikev1_policy(desired_data)
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
        result = dev.delete_ikev1_policy(name)
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
            priority=dict(required=True),
            state=dict(required=True, choices=['absent', 'present']),
            authentication=dict(required=False, choices=['pre-share', 'rsa-sig']),
            encryption=dict(required=False, choices=['des', '3des', 'aes-128', 'aes-192', 'aes-256']),
            hash=dict(required=False, choices=['md5', 'sha']),
            group=dict(required=False, choices=['1', '2', '5']),
            validate_certs=dict(required=False, choices=['no', 'yes'], default='yes'),
            lifetime=dict(required=False),
            ),
            required_together = ( ['authentication', 'encryption', 'hash', 'group', 'lifetime'],),
        supports_check_mode=False)

    m_args = module.params

    if not has_rasa:
        module.fail_json(msg='Missing required rasa module (check docs)')

    if m_args['state'] == "present" and m_args['authentication'] == False:
        module.fail_json(msg='Authentication mode not defined')

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

    try:
        priority = int(m_args['priority'])
    except:
        module.fail_json(msg='Priority has to be a number')

    if 1 <= priority <= 65535:
        #desired_data['priority'] = m_args['priority']
        desired_data['priority'] = priority
        desired_data['objectId'] = m_args['priority']
    else:
        module.fail_json(msg='Priority must be between 1 and 65535')

    if m_args['state'] == "present":

        try:
            lifetime = int(m_args['lifetime'])
        except:
            module.fail_json(msg='Lifetime has to be a number')

        if 120 <= lifetime <= 2147483647:
            desired_data['lifetimeInSecs'] = lifetime
        else:
            module.fail_json(msg='Lifetime must be between 120 and 2147483647')

        desired_data['authentication'] = m_args['authentication']
        desired_data['encryption'] = m_args['encryption']
        desired_data['hash'] = m_args['hash']
        desired_data['dhgroup'] = int(m_args['group'])
        desired_data['kind'] = 'object#ikev1policy'
        desired_data['objectId'] = m_args['priority']
        desired_data['selfLink'] = 'https://%s/api/vpn/ikev1policy/%s' % (m_args['host'], m_args['priority'])

    try:
        data = dev.get_ikev1_policy(m_args['priority'])
    except:
        err = sys.exc_info()[0]
        module.fail_json(msg='Unable to connect to device: %s' % err)

    if data.status_code == 200:
        
        if m_args['state'] == 'absent':

            changed_status = delete_object(dev, module, m_args['priority'])

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
    for key in current_data:
        if current_data[key] != desired_data[key]:
            return False
    return True


def update_object(dev, module, desired_data):
    try:
        result = dev.update_ikev1_policy(desired_data['objectId'], desired_data)
    except:
        err = sys.exc_info()[0]
        module.fail_json(msg='Unable to connect to device: %s' % err)

    if result.status_code == 204:
        return_status = { 'changed': True }
    else:
        module.fail_json(msg='Unable to update object code: - %s' % result.status_code)

    return return_status



main()

