python generator.py  --cluster amino
ansible-playbook -u stack -i cluster/amino/.ansible/hosts playbooks/prepare_node.yaml -s
ansible-playbook -u stack -i cluster/amino/.ansible/java/hosts cluster/amino/.ansible/java/install.yaml -s 
ansible-playbook -u stack -i cluster/amino/.ansible/zookeeper/hosts cluster/amino/.ansible/zookeeper/install.yaml -s
ansible-playbook -u stack -i cluster/amino/.ansible/hadoop/hosts cluster/amino/.ansible/hadoop/install.yaml -s
ansible-playbook -u stack -i cluster/amino/.ansible/hadoop/hosts cluster/amino/.ansible/hadoop/install.yaml -s -e "sync_release=no"

ansible -u stack -i cluster/amino/.ansible/hosts zookeeper_server -m shell -a "systemctl start zookeeper_server" -s
ansible -u stack -i cluster/amino/.ansible/hosts journalnode -m shell -a "systemctl start journalnode" -s

Active NN:
sudo to hdfs
/apache/hadoop/bin/hdfs zkfc -formatZK
/apache/hadoop/bin/hdfs namenode -format
sudo to root
systemctl start zkfc
systemctl start namenode

Standby NN:
sudo to hdfs
/apache/hadoop/bin/hdfs namenode -bootstrapStandby

ansible -u stack -i cluster/amino/.ansible/hosts resource_manager -m shell -a "systemctl start resource_manager" -s
ansible -u stack -i cluster/amino/.ansible/hosts resource_manager -m shell -a "systemctl start nodemanager" -s