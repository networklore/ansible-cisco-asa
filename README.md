## About

Repo containing [Ansible](https://github.com/ansible/ansible) modules for Cisco ASA using the REST API which appeared in ASA 9.3.

Over at Networklore there's more information about the [Ansible modules for Cisco ASA](http://networklore.com/ansible-cisco-asa/).

## Alpha code

Currently this is only a test and there's a good chance that a lot of the code will change.

## Dependencies

These modules requires:

* [rasa](https://github.com/networklore/rasa) 0.0.5 or later
* An ASA firewall running 9.3 or later

## Current modules

* cisco_asa_ikev1_policy
* cisco_asa_network_object
* cisco_asa_network_objectgroup
* cisco_asa_write_mem

## Installation of Ansible module
```
pip install rasa
```
As new modules are added you will need to update rasa to support newer features.
```
pip install rasa --upgrade
```
If you are running Ansible through a Python virtualenv you might need to change the ansible_python_interpreter variable. Check the hosts file in this repo for an example. You can clone this repo and copy the modules to your Ansible library path.

## Known issues

* Changing service object types doesn't work. I.e. changing an "object service" from tcp/udp/icmp to a network protocol.

## Feedback

If you have any questions or feedback. Please send me a note over [at my blog](http://networklore.com/contact/) or submit an issue here at Github.