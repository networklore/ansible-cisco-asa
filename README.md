## Project abandoned

As I wrote on the [Rasa](https://github.com/networklore/rasa) repo this project has been abandoned, this code is only left as reference.

## About

Repo containing [Ansible](https://github.com/ansible/ansible) modules for Cisco ASA using the REST API which appeared in ASA 9.3.

Over at Networklore there's more information about the [Ansible modules for Cisco ASA](http://networklore.com/ansible-cisco-asa/).

## Dependencies

These modules requires:

* [rasa](https://github.com/networklore/rasa) 0.0.5 or later
* An ASA firewall running 9.3 or later

## Current modules

* cisco_asa_ikev1_policy
* cisco_asa_network_object
* cisco_asa_network_objectgroup
* cisco_asa_write_mem

## Known issues

* Changing service object types doesn't work. I.e. changing an "object service" from tcp/udp/icmp to a network protocol.

## Feedback

If you have any questions or feedback. Please send me a note over [at my blog](http://networklore.com/contact/) or submit an issue here at Github.
