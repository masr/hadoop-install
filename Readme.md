#Generate files
python generator.py  --cluster amino


#Installation
export ANSIBLE_HOST_KEY_CHECKING=False

ansible-playbook -u stack -i cluster/amino/.ansible/hosts playbooks/prepare_node.yaml -b -e @cluster/amino/.ansible/vars.yaml

ansible-playbook -u stack -i cluster/amino/.ansible/java/hosts cluster/amino/.ansible/java/install.yaml -b 

ansible-playbook -u stack -i cluster/amino/.ansible/zookeeper/hosts cluster/amino/.ansible/zookeeper/install.yaml -b

ansible-playbook -u stack -i cluster/amino/.ansible/hadoop/hosts cluster/amino/.ansible/hadoop/install.yaml -b

ansible-playbook -u stack -i cluster/amino/.ansible/spark/hosts cluster/amino/.ansible/spark/install.yaml -b

ansible-playbook -u stack -i cluster/amino/.ansible/hadoop/hosts cluster/amino/.ansible/hadoop/install.yaml -b -e "sync_release=no"

ansible -u stack -i cluster/amino/.ansible/hosts zookeeper -m shell -a "systemctl start zookeeper" -b

ansible -u stack -i cluster/amino/.ansible/hosts journalnode -m shell -a "systemctl start journalnode" -b

#Active NN:

sudo to hdfs

/apache/hadoop/bin/hdfs zkfc -formatZK

/apache/hadoop/bin/hdfs namenode -format

sudo to root

systemctl start zkfc

systemctl start namenode

# Standby NN:

sudo to hdfs

/apache/hadoop/bin/hdfs namenode -bootstrapStandby

sudo to root

systemctl start zkfc

# Start DN
ansible -u stack -i cluster/amino/.ansible/hosts datanode -m shell -a "systemctl start datanode" -b

#Start RM
ansible -u stack -i cluster/amino/.ansible/hosts resourcemanager -m shell -a "systemctl start resourcemanager" -b

#Start NM
ansible -u stack -i cluster/amino/.ansible/hosts nodemanager -m shell -a "systemctl start nodemanager" -b