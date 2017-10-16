# ACC: Airfoil Project G14
This project was developed as final project for the course Applied Cloud Computing.

## File structure:

### orchestration:
This folder contains the following YAML scripts for the application deployment using Heat orchestrator and Cloud-init contextualizer:
- airfoil_asg_g14.yaml: Airfoil stack with auto-scaling group
- airfoil_rg_g14.yaml: Airfoil stack with resource group
- client_g14.txt: Celery client contextualization file
- worker_rg_g14.yaml: Celery worker resource group
- worker_g14.txt: Celery worker contextualization file
- environment.yaml: Celery worker resource registration

## Deployment Instructions
- Using resource group: openstack stack create -t airfoil_stack_g14.yaml airfoil_stack_g14
- Using auto-scaling group: openstack stack create -t airfoil_asg_g14.yaml -e environment.yaml airfoil_asg_g14

You could also change the default values for any of the following parameters including --parameter "ParamName=ParamValue"
- image:  Image to be used for compute instance
- flavor: Type of instance (flavor) to be used
- key: Name of key-pair to be used for compute instance
- public_network: Public network with floating IP addresses
- internal_network: SNIC 2017/13-45 Internal IPv4 Network
- workers: Number of celery worker nodes to be deployed.
- sec_group_name: Assigned name for the security group.

## Task Monitoring
To monitor task execution using celery flower visit:
<floatingip_client_node>:5555
