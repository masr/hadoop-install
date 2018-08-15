#!/usr/bin/python

import argparse
import yaml
from processor.hadoop_process import HadoopProcess
from processor.java_process import JavaProcess
from processor.zookeeper_process import ZookeeperProcess
from processor.spark_process import SparkProcess
from processor.topology import Topology
from constants import SERVICE, ROLE

parser = argparse.ArgumentParser(description='Generate Configs')
parser.add_argument('--cluster', help='cluster name', required=True)
args = parser.parse_args()
print("Generating config for cluster: " + args.cluster + "\n")
cluster = args.cluster
with open("cluster/" + cluster + "/config/topology.yaml") as topology_file:
    topology_data = yaml.load(topology_file.read(), Loader=yaml.Loader)
    topology = Topology(topology_data)

SERVICE_TO_PROCESS = {
    SERVICE.JAVA: JavaProcess(cluster, topology),
    SERVICE.HADOOP: HadoopProcess(cluster, topology),
    SERVICE.ZOOKEEPER: ZookeeperProcess(cluster, topology),
    SERVICE.SPARK: SparkProcess(cluster, topology)
}
required_services = set()
with open('cluster/' + cluster + '/.ansible/hosts', "w") as tmp_file:
    for role_name, role in ROLE.__members__.items():
        tmp_file.write("[" + role.value + "]\n")
        tmp_file.write('\n'.join(topology.get_hosts_of_role(role)) + '\n\n')
    tmp_file.write("[all]\n")
    tmp_file.write('\n'.join(topology.get_all_hosts()))

for _, service_type in SERVICE.__members__.items():
    hosts = topology.get_hosts_of_service(service_type)
    if len(hosts) > 0:
        if service_type in SERVICE_TO_PROCESS:
            process = SERVICE_TO_PROCESS[service_type]
            process.generate_configs()
            process.generate_ansible()
