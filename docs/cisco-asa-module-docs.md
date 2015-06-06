# Cisco ASA Ansible Module Docs
### *Manage Cisco ASA devices with Ansible using the ASA REST API*

---
### Requirements
 * Check the [README](../README.md#Dependencies)

---
### Modules

  * [cisco_asa_ikev1_policy - creates deletes or edits ikev1 policies.](#cisco_asa_ikev1_policy)
  * [cisco_asa_network_object - creates deletes or edits network objects.](#cisco_asa_network_object)
  * [cisco_asa_network_objectgroup - creates deletes or edits network object-groups.](#cisco_asa_network_objectgroup)
  * [cisco_asa_write_mem - saves the configuration.](#cisco_asa_write_mem)

---

## cisco_asa_ikev1_policy
Creates deletes or edits ikev1 policies.

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Creates deletes or edits ikev1 policies.

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | |  Username for device  |
| hash  |   no  |  | <ul> <li>md5</li>  <li>sha</li> </ul> |  Hash Algorithm  |
| encryption  |   no  |  | <ul> <li>des</li>  <li>3des</li>  <li>aes-128</li>  <li>aes-192</li>  <li>aes-256</li> </ul> |  Encryption Algorithm  |
| state  |   yes  |  | <ul> <li>present</li>  <li>absent</li> </ul> |  State of the object  |
| group  |   no  |  | <ul> <li>1</li>  <li>2</li>  <li>5</li> </ul> |  Diffie-Hellman group  |
| priority  |   yes  |  | <ul> <li>1-65535</li> </ul> |  The priority number of the ikev1 policy.  |
| authentication  |   no  |  | <ul> <li>pre-share</li>  <li>rsa-sig</li> </ul> |  Authentication method  |
| host  |   yes  |  | |  Typically set to {# inventory_hostname #}  |
| lifetime  |   yes  |  | <ul> <li>120-2147483647</li> </ul> |  SA Lifetime (seconds)  |
| password  |   yes  |  | |  Password for the device  |
| validate_certs  |   no  |  | <ul> <li>no</li>  <li>yes</li> </ul> |  If no, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.  |

#### Examples
```

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

```


---


## cisco_asa_network_object
Creates deletes or edits network objects.

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Configures network objects

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| category  |   no  |  | <ul> <li>ipv4_address</li>  <li>ipv6_address</li>  <li>ipv4_subnet</li>  <li>ipv6_subnet</li>  <li>ipv4_range</li>  <li>ipv6_range</li>  <li>ipv4_fqdn</li>  <li>ipv6_fqdn</li> </ul> |  The type of object you are creating. Use slash notation for subnets, i.e. 192.168.0.0/24. Use - for ranges, i.e. 192.168.0.1-192.168.0.10.  |
| username  |   yes  |  | |  Username for device  |
| description  |   no  |  | |  Description of the object  |
| state  |   yes  |  | <ul> <li>present</li>  <li>absent</li> </ul> |  State of the object  |
| value  |   no  |  | |  The data to enter into the network object  |
| host  |   yes  |  | |  Typically set to {# inventory_hostname #}  |
| password  |   yes  |  | |  Password for the device  |
| validate_certs  |   no  |  | <ul> <li>no</li>  <li>yes</li> </ul> |  If no, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.  |
| name  |   yes  |  | |  Name of the network object  |

#### Examples
```

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

```


---


## cisco_asa_network_objectgroup
Creates deletes or edits network object-groups.

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Configures network object-groups

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| category  |   no  |  | <ul> <li>ipv4_address</li>  <li>ipv6_address</li>  <li>ipv4_subnet</li>  <li>ipv6_subnet</li>  <li>ipv4_range</li>  <li>ipv6_range</li>  <li>ipv4_fqdn</li>  <li>ipv6_fqdn</li>  <li>object</li>  <li>object_group</li> </ul> |  The type of object you are creating. Use slash notation for networks, i.e. 192.168.0.0/24. Use - for ranges, i.e. 192.168.0.1-192.168.0.10.  |
| username  |   yes  |  | |  Username for device  |
| name  |   yes  |  | |  Name of the network object  |
| entry_state  |   no  |  | <ul> <li>present</li>  <li>absent</li> </ul> |  State of the entire object-group  |
| value  |   no  |  | |  The data to enter into the network object  |
| state  |   yes  |  | <ul> <li>present</li>  <li>absent</li> </ul> |  State of the entire object-group  |
| members  |   no  |  | |  NOT YET IMPLEMENTED Variable containing all the objects within the network object-group  |
| host  |   yes  |  | |  Typically set to {# inventory_hostname #}  |
| password  |   yes  |  | |  Password for the device  |
| validate_certs  |   no  |  | <ul> <li>no</li>  <li>yes</li> </ul> |  If no, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.  |
| description  |   no  |  | |  Description of the object  |

#### Examples
```

# Create a network object for a web server
- cisco_asa_network_object:
    host={{ inventory_hostname }}
    username=api_user
    password=APIpass123
    name=tsrv-web-1
    state=present
    category=IPv4Address
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

```


---


## cisco_asa_write_mem
Saves the configuration.

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Issues the write mem command on the unit

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| username  |   yes  |  | |  Username for device  |
| host  |   yes  |  | |  Typically set to {# inventory_hostname #}  |
| password  |   yes  |  | |  Password for the device  |
| validate_certs  |   no  |  | <ul> <li>no</li>  <li>yes</li> </ul> |  If no, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.  |

#### Examples
```

# Save the running configuration
- cisco_asa_write_mem:
    host={{ inventory_hostname }}
    username=api_user
    password=APIpass123
    validate_certs=no


```


---


---
Documentation generated with [Ansible Webdocs](https://github.com/jedelman8/ansible-webdocs).
