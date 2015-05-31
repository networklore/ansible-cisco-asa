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
short_description: Creates deletes or edits network objects.
version: 0.x
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
    dst_port:
        description:
            - Destination port. Usable when protocol is set to tcp, udp or icmp
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
    protocol:
        description:
            - Protocol
        required: False
    src_port:
        description:
            - Source port. Usable when protocol is set to tcp or udp.
        required: false
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
    from rasa.constants import ip_protocol_name, tcp_services, udp_services
    has_rasa = True
except:
    has_rasa = False

protocols_using_ports = ['tcp', 'udp']

def create_object(dev, module, desired_data):
    try:
        result = dev.create_serviceobject(desired_data)
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
        result = dev.delete_serviceobject(name)
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
            dst_port=dict(required=False),
            src_port=dict(required=False),
            icmp_type=dict(required=False),
            icmp_code=dict(required=False),
            state=dict(required=True, choices=['absent', 'present']),
            protocol=dict(required=False, choices=[
                'ah', 'eigrp','esp','gre','icmp','icmp6','igmp', 'igrp',
                'ip', 'ipinip', 'ipsec', 'nos', 'ospf', 'pcp', 'pim',
                'pptp', 'snp', 'tcp', 'udp',
                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11',
                '12', '13', '14', '15', '16', '17', '18', '19', '20', '21',
                '22', '23', '24', '25', '26', '27', '28', '29', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '40', '41',
                '42', '43', '44', '45', '46', '47', '48', '49', '50', '51',
                '52', '53', '54', '55', '56', '57', '58', '59', '60', '61',
                '62', '63', '64', '65', '66', '67', '68', '69', '70', '71',
                '72', '73', '74', '75', '76', '77', '78', '79', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '90', '91',
                '92', '93', '94', '95', '96', '97', '98', '99', '100', '101',
                '102', '103', '104', '105', '106', '107', '108', '109', '110',
                '111', '112', '113', '114', '115', '116', '117', '118', '119',
                '120', '121', '122', '123', '124', '125', '126', '127', '128',
                '129', '130', '131', '132', '133', '134', '135', '136', '137',
                '138', '139', '140', '141', '142', '143', '144', '145', '146',
                '147', '148', '149', '150', '151', '152', '153', '154', '155',
                '156', '157', '158', '159', '160', '161', '162', '163', '164',
                '165', '166', '167', '168', '169', '170', '171', '172', '173',
                '174', '175', '176', '177', '178', '179', '180', '181', '182',
                '183', '184', '185', '186', '187', '188', '189', '190', '191',
                '192', '193', '194', '195', '196', '197', '198', '199', '200',
                '201', '202', '203', '204', '205', '206', '207', '208', '209',
                '210', '211', '212', '213', '214', '215', '216', '217', '218',
                '219', '220', '221', '222', '223', '224', '225', '226', '227',
                '228', '229', '230', '231', '232', '233', '234', '235', '236',
                '237', '238', '239', '240', '241', '242', '243', '244', '245',
                '246', '247', '248', '249', '250', '251', '252', '253', '254',
                '255',]),
            validate_certs=dict(required=False, choices=['no', 'yes'], default='yes'),
            value=dict(required=False)),
            required_together = ( ['category','value'],),
        supports_check_mode=False)

    m_args = module.params

    if not has_rasa:
        module.fail_json(msg='Missing required rasa module (check docs)')

    if m_args['state'] == "present":
        if m_args['protocol'] == False:
            module.fail_json(msg='Protocol not defined')
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

    if m_args['src_port'] and m_args['protocol'] not in protocols_using_ports:
        module.fail_json(msg="Can't use source port with %s" % m_args['protocol'])

    if m_args['dst_port'] and m_args['protocol'] not in protocols_using_ports:
        module.fail_json(msg="Can't use destination port with %s" % m_args['protocol'])


    # icmp -> ICMPServiceObj
    # icmp6 -> object#ICMP6ServiceObj
    if m_args['dst_port'] or m_args['src_port']:
        kind = 'object#TcpUdpServiceObj'
    elif m_args['protocol']:
        kind = 'object#NetworkProtocolObj'

        protocol = m_args['protocol']
        try:
            protocol = int(m_args['protocol'])
        except:
            pass
        if isinstance(protocol, int):
            protocol = ip_protocol_name[str(protocol)]
    else:
        kind = 'object#NetworkProtocolObj'

    # Change to function to target source dest udp and tcp
    if m_args['dst_port'] and m_args['protocol'] == 'tcp':
        try:
            int(m_args['dst_port'])
        except:
            if m_args['dst_port'] not in tcp_services.itervalues():
                module.fail_json(msg='%s is not valid using tcp' % m_args['dst_port'])

        if isinstance(m_args['dst_port'], int):
            if 1 <= m_args['dst_port'] <= 65535:
                m_args['dst_port'] = str(m_args['dst_port'])
            else:
                module.fail_json(msg='%s is not a valid tcp port' % m_args['dst_port'])


    desired_data = {}
    desired_data['name'] = m_args['name']
    desired_data['objectId'] = m_args['name']
    desired_data['kind'] = kind

    if kind == 'object#NetworkProtocolObj':
        desired_data['value'] = protocol
    elif kind == 'object#TcpUdpServiceObj':
        # Fix for source ports too
        desired_data['value'] = '%s/%s' % (m_args['protocol'], m_args['dst_port'])

    if m_args['description']:
        desired_data['description'] = m_args['description']

    try:
        data = dev.get_serviceobject(m_args['name'])
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

    if current_data['kind'] != desired_data['kind']:
        return False

    if current_data['value'] != desired_data['value']:
        return False

    return True


def update_object(dev, module, desired_data):
    try:
        result = dev.update_serviceobject(desired_data['name'], desired_data)
    except:
        err = sys.exc_info()[0]
        module.fail_json(msg='Unable to connect to device: %s' % err)

    if result.status_code == 204:
        return_status = True
    else:
        module.fail_json(msg='Unable to update object code: - %s - %s' % (result.status_code, desired_data))

    return return_status



main()

