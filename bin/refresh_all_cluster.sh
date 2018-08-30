sync_release=$1

./bin/generator.sh --cluster amino
./bin/generator.sh --cluster compute_on_aws


ansible-playbook -u ec2-user -i cluster/amino/.ansible/java/hosts cluster/amino/.ansible/java/install.yaml -b -e "sync_release=$sync_release"
ansible-playbook -u ec2-user -i cluster/compute_on_aws/.ansible/java/hosts cluster/compute_on_aws/.ansible/java/install.yaml -b -e "sync_release=$sync_release"


ansible-playbook -u ec2-user -i cluster/amino/.ansible/zookeeper/hosts cluster/amino/.ansible/zookeeper/install.yaml -b -e "sync_release=$sync_release"
ansible-playbook -i cluster/amino/.ansible/hosts playbooks/stop_zookeeper.yaml -u ec2-user -b
ansible-playbook -i cluster/amino/.ansible/hosts playbooks/start_zookeeper.yaml -u ec2-user -b

ansible-playbook -u ec2-user -i cluster/amino/.ansible/hadoop/hosts cluster/amino/.ansible/hadoop/install.yaml -b -e "sync_release=$sync_release"
ansible-playbook -i cluster/amino/.ansible/hosts playbooks/stop_hdfs.yaml -u ec2-user -b
ansible-playbook -i cluster/amino/.ansible/hosts playbooks/start_hdfs.yaml -u ec2-user -b
ansible-playbook -i cluster/amino/.ansible/hosts playbooks/stop_jobhistoryserver.yaml -u ec2-user -b
ansible-playbook -i cluster/amino/.ansible/hosts playbooks/start_jobhistoryserver.yaml -u ec2-user -b


ansible-playbook -u ec2-user -i cluster/compute_on_aws/.ansible/hadoop/hosts cluster/compute_on_aws/.ansible/hadoop/install.yaml -b -e "sync_release=$sync_release"
ansible-playbook -i cluster/compute_on_aws/.ansible/hosts playbooks/stop_yarn.yaml -u ec2-user -b
ansible-playbook -i cluster/compute_on_aws/.ansible/hosts playbooks/start_yarn.yaml -u ec2-user -b

ansible-playbook -u ec2-user -i cluster/amino/.ansible/spark/hosts cluster/amino/.ansible/spark/install.yaml -b -e "sync_release=$sync_release"
ansible-playbook -i cluster/amino/.ansible/hosts playbooks/stop_spark.yaml -u ec2-user -b
ansible-playbook -i cluster/amino/.ansible/hosts playbooks/start_spark.yaml -u ec2-user -b

ansible-playbook -u ec2-user -i cluster/compute_on_aws/.ansible/spark/hosts cluster/compute_on_aws/.ansible/spark/install.yaml -b -e "sync_release=$sync_release"

ansible-playbook -u ec2-user -i cluster/amino/.ansible/hive/hosts cluster/amino/.ansible/hive/install.yaml -b -e "sync_release=$sync_release"
ansible-playbook -i cluster/compute_on_aws/.ansible/hosts playbooks/stop_hive.yaml -u ec2-user -b
ansible-playbook -i cluster/compute_on_aws/.ansible/hosts playbooks/start_hive.yaml -u ec2-user -b

ansible-playbook -u ec2-user -i cluster/compute_on_aws/.ansible/hive/hosts cluster/compute_on_aws/.ansible/hive/install.yaml -b -e "sync_release=$sync_release"
