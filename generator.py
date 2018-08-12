#!/usr/bin/python

import argparse
import yaml
from processor.hadoop_process import HadoopProcess
from processor.java_process import JavaProcess
from processor.zookeeper_process import ZookeeperProcess
from processor.topology import Topology
from constants import SERVICE, ALL_ROLES

parser = argparse.ArgumentParser(description='Generate Configs')
parser.add_argument('--cluster', help='cluster name', required=True)
args = parser.parse_args()
print("Generating config for cluster: " + args.cluster + "\n")
cluster = args.cluster
with open("cluster/" + cluster + "/config/topology.yaml") as topology_file:
    topology_data = yaml.load(topology_file.read(), Loader=yaml.Loader)
    topology = Topology(topology_data)

# service_exists_dict = dict()
# service_exists_dict[SERVICE.HADOOP] = 'namenodes' in topology_roles or 'resource_managers' in topology_roles
# service_exists_dict[SERVICE.ZOOKEEPER] = 'zookeeper_servers' in topology_roles
# service_exists_dict[SERVICE.HBASE] = 'hbase_masters' in topology_roles
# service_exists_dict[SERVICE.HIVE] = 'hive_metastores' in topology_roles
# service_exists_dict[SERVICE.SPARK] = 'spark_clis' in topology_roles

with open('cluster/' + cluster + '/.ansible/hosts', "w") as tmp_file:
    for role in ALL_ROLES:
        tmp_file.write("[" + role + "]\n")
        tmp_file.write('\n'.join(topology.get_hosts_of_role(role)) + '\n\n')
    tmp_file.write("[all]\n")
    tmp_file.write('\n'.join(topology.get_all_hosts()))

for name, value in SERVICE.__members__.items():
    if value == SERVICE.HADOOP:
        java_process = JavaProcess(cluster, topology_data)
        java_process.generate_configs()
        java_process.generate_ansible()
        hadoop_process = HadoopProcess(cluster, topology_data)
        hadoop_process.generate_configs()
        hadoop_process.generate_ansible()
        zookeeper_process = ZookeeperProcess(cluster, topology_data)
        zookeeper_process.generate_configs()
        zookeeper_process.generate_ansible()
