from constants import SERVICE, ROLE
from processor.abstract_process import AbstractProcess
from processor.utils import replace_params, trans_dict_to_conf, replace_values_in_dict


class ZookeeperProcess(AbstractProcess):
    def __init__(self, cluster_name, topology):
        AbstractProcess.__init__(self, cluster_name, SERVICE.ZOOKEEPER, topology)

    def get_all_parsed_configs(self, group_name):
        mapping = self.parse_configs(group_name)
        mapping['zoo.cfg'] = trans_dict_to_conf(mapping['zoo.cfg'])
        return mapping

    def parse_configs(self, group_name):
        basic_config = self.get_merged_basic_configuration_by_group(group_name)

        mapping = {}
        ################## zoo.cfg **********************************
        zookeeper_servers = self.topology.get_hosts_of_role(ROLE.ZOOKEEPER_SERVER)
        data = self.get_merged_service_configuration_by_group('zoo.yaml', group_name)
        for zookeeper_server in zookeeper_servers:
            vars_dict = self.topology.get_vars_from_host(zookeeper_server)
            data["server." + str(vars_dict['zookeeper_myid'])] = zookeeper_server + ':2888:3888'

        mapping['zoo.cfg'] = replace_values_in_dict(data, basic_config)

        ################## zookeeper-env.sh **********************************
        data = self.get_text_template('zookeeper-env.sh')
        mapping['zookeeper-env.sh'] = replace_params(data, basic_config)

        ################# log4j.properties ###########################
        data = self.get_text_template('log4j.properties')
        mapping['log4j.properties'] = replace_params(data, basic_config)

        return mapping

    def get_all_kv_from_config(self, group_name):
        return {}
