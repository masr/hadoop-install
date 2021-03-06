#!/usr/bin/python

import argparse

import yaml

from hadoop_install.constants import SERVICE, ROLE
from hadoop_install.processor.hadoop_process import HadoopProcess
from hadoop_install.processor.java_process import JavaProcess
from hadoop_install.processor.nil_process import NilProcess
from hadoop_install.processor.spark_process import SparkProcess
from hadoop_install.processor.zookeeper_process import ZookeeperProcess
from hadoop_install.processor.hive_process import HiveProcess
from hadoop_install.topology import Topology
from hadoop_install.utils import check_and_create_dir

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
    SERVICE.SPARK: SparkProcess(cluster, topology),
    SERVICE.HIVE: HiveProcess(cluster, topology)
}

check_and_create_dir('cluster/' + cluster + '/.ansible')
with open('cluster/' + cluster + '/.ansible/hosts', "w") as tmp_file:
    for role_name, role in ROLE.__members__.items():
        tmp_file.write("[" + role.value + "]\n")
        tmp_file.write('\n'.join(topology.get_hosts_of_role(role)) + '\n\n')
    tmp_file.write("[all]\n")
    tmp_file.write('\n'.join(topology.get_all_hosts()))

nil_process = NilProcess(cluster, topology)
vars = nil_process.get_merged_basic_configuration_by_group('default')
with open('cluster/' + cluster + '/.ansible/vars.yaml', 'w') as tmp_file:
    content = yaml.dump(vars, default_flow_style=False)
    tmp_file.write(content)

for _, service_type in SERVICE.__members__.items():
    hosts = topology.get_hosts_of_service(service_type)
    if len(hosts) > 0:
        if service_type in SERVICE_TO_PROCESS:
            process = SERVICE_TO_PROCESS[service_type]
            process.generate_configs()
            process.generate_ansible()
