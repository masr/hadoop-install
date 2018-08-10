python generator.py  --cluster amino
ansible-playbook -u stack -i cluster/amino/.ansible/hosts playbooks/prepare_node.yaml -s
ansible-playbook -u stack -i cluster/amino/.ansible/java/hosts cluster/amino/.ansible/java/install.yaml -s 
ansible-playbook -u stack -i cluster/amino/.ansible/hadoop/hosts cluster/amino/.ansible/hadoop/install.yaml -s