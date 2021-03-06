from hadoop_install.constants import SERVICE, ROLE
from hadoop_install.processor.abstract_process import AbstractProcess
from hadoop_install.utils import replace_params, trans_dict_to_conf, replace_values_in_dict


class ZookeeperProcess(AbstractProcess):
    def __init__(self, cluster_name, topology):
        AbstractProcess.__init__(self, cluster_name, SERVICE.ZOOKEEPER, topology)

    def get_all_parsed_configs(self, group_name):
        mapping, basic_config = self.parse_configs(group_name)
        mapping['zoo.cfg'] = trans_dict_to_conf(mapping['zoo.cfg'])
        return mapping, basic_config

    def parse_configs(self, group_name):
        basic_config = self.get_merged_basic_configuration_by_group(group_name)

        mapping = {}
        ################## zoo.cfg **********************************
        zookeepers = self.topology.get_hosts_of_role(ROLE.ZOOKEEPER)
        data = self.get_merged_service_configuration_by_group('zoo.yaml', group_name)
        for zookeeper in zookeepers:
            vars_dict = self.topology.get_vars_from_host(zookeeper)
            data["server." + str(vars_dict['zookeeper_myid'])] = zookeeper + ':2888:3888'

        mapping['zoo.cfg'] = data

        ################## zookeeper-env.sh **********************************
        mapping['zookeeper-env.sh'] = self.get_text_template('zookeeper-env.sh')

        ################# log4j.properties ###########################
        mapping['log4j.properties'] = self.get_text_template('log4j.properties')

        return mapping, basic_config

    def get_all_kv_from_config(self, group_name):
        return {}
