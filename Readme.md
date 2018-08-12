python generator.py  --cluster amino
ansible-playbook -u stack -i cluster/amino/.ansible/hosts playbooks/prepare_node.yaml -s
ansible-playbook -u stack -i cluster/amino/.ansible/java/hosts cluster/amino/.ansible/java/install.yaml -s 
ansible-playbook -u stack -i cluster/amino/.ansible/zookeeper/hosts cluster/amino/.ansible/zookeeper/install.yaml -s
ansible-playbook -u stack -i cluster/amino/.ansible/hadoop/hosts cluster/amino/.ansible/hadoop/install.yaml -s
ansible-playbook -u stack -i cluster/amino/.ansible/hadoop/hosts cluster/amino/.ansible/hadoop/install.yaml -s -e "sync_release=no"

ansible -u stack -i cluster/amino/.ansible/zookeeper/hosts zookeeper_server -m shell -a "systemctl start zookeeper_server" -s