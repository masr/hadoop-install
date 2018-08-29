#Generate files
python generator.py  --cluster amino


#Installation
export ANSIBLE_HOST_KEY_CHECKING=False

ansible-playbook -u ec2-user -i cluster/amino/.ansible/hosts playbooks/prepare_node.yaml -b -e @cluster/amino/.ansible/vars.yaml

ansible-playbook -u ec2-user -i cluster/amino/.ansible/java/hosts cluster/amino/.ansible/java/install.yaml -b 

ansible-playbook -u ec2-user -i cluster/amino/.ansible/zookeeper/hosts cluster/amino/.ansible/zookeeper/install.yaml -b

ansible-playbook -u ec2-user -i cluster/amino/.ansible/hadoop/hosts cluster/amino/.ansible/hadoop/install.yaml -b

ansible-playbook -u ec2-user -i cluster/amino/.ansible/hadoop/hosts cluster/amino/.ansible/hadoop/install.yaml -b -e "sync_release=no"

ansible-playbook -u ec2-user -i cluster/amino/.ansible/spark/hosts cluster/amino/.ansible/spark/install.yaml -b

ansible-playbook -u ec2-user -i cluster/amino/.ansible/hive/hosts cluster/amino/.ansible/hive/install.yaml -b

ansible -u ec2-user -i cluster/amino/.ansible/hosts zookeeper -m shell -a "systemctl start zookeeper" -b

ansible -u ec2-user -i cluster/amino/.ansible/hosts journalnode -m shell -a "systemctl start journalnode" -b

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

systemctl start namenode

# Start DN
ansible -u ec2-user -i cluster/amino/.ansible/hosts datanode -m shell -a "systemctl start datanode" -b

hadoop fs -mkdir /spark-logs
hadoop fs -chown spark:hadoop /spark-logs

hadoop fs -mkdir /yarn-logs
hadoop fs -chown yarn:hadoop /yarn-logs

#Prepare for YARN
hadoop fs -mkdir /yarn-logs
hadoop fs -chmod 777 /yarn-logs
hadoop fs -chown yarn:hadoop /yarn-logs

#Start RM
ansible -u ec2-user -i cluster/amino/.ansible/hosts resourcemanager -m shell -a "systemctl start resourcemanager" -b

#Start NM
ansible -u ec2-user -i cluster/amino/.ansible/hosts nodemanager -m shell -a "systemctl start nodemanager" -b

#Prepare for spark
hadoop fs -mkdir /spark-logs
hadoop fs -chmod 777 /spark-logs
hadoop fs -chown spark:hadoop /spark-logs

# Start Spark History Server
ansible -u ec2-user -i cluster/amino/.ansible/hosts sparkhistoryserver -m shell -a "systemctl start sparkhistoryserver" -b

# Start Job Jistory Server
ansible -u ec2-user -i cluster/amino/.ansible/hosts jobhistoryserver -m shell -a "systemctl start jobhistoryserver" -b


# Prepare for hive
hadoop credential create javax.jdo.option.ConnectionPassword -provider jceks://file/tmp/hive.jceks
cp /tmp/hive.jceks cluster/amino/config/hive/hive.jceks

/apache/hive/bin/schematool -dbType mysql -initSchema

hadoop fs -mkdir /user/hive
hadoop fs -chown hive:hadoop /user/hive
hadoop fs -mkdir /user/hive/warehouse
hadoop fs -chown hive:hadoop /user/hive/warehouse
hadoop fs -chmod 777 /user/hive/warehouse

# Start Hive Metastore
ansible -u ec2-user -i cluster/amino/.ansible/hosts hivemetastore -m shell -a "systemctl start hivemetastore" -b

# Run Spark on S3 
export AWS_ACCESS_KEY_ID='xxxx'
export AWS_SECRET_ACCESS_KEY='xxxx'
/apache/spark/bin/spark-shell --num-executors 1 --executor-memory 1G

val df=spark.read
.format("text")
.load("s3a://maosuhan-amino/test/*")
.flatMap(row => row.getString(0).split(" "))
.map(word => (word,1))
.toDF("word", "freq")
.createOrReplaceTempView("word")

resultDF=spark.sql("select word,count(*) from word group by word")