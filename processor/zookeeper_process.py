from constants import SERVICE
from processor.abstract_process import AbstractProcess
from processor.utils import replace_params


class ZookeeperProcess(AbstractProcess):
    def __init__(self, cluster_name, topology_data):
        AbstractProcess.__init__(self, cluster_name, SERVICE.ZOOKEEPER, topology_data)

    def get_all_parsed_configs(self, group_name):
        mapping = self.parse_configs(group_name)
        return mapping

    def parse_configs(self, group_name):
        basic_config = self.get_merged_basic_configuration_by_group(group_name)

        mapping = {}
        ################## zoo.cfg **********************************
        data = self.get_text_template('zoo.cfg')
        zookeeper_servers = self.topology.get_hosts_of_role('zookeeper_server')
        zookeeper_definition_content = ''
        for zookeeper_server in zookeeper_servers:
            vars_dict = self.topology.get_vars_from_host(zookeeper_server)
            zookeeper_definition_content += \
                "server." + str(vars_dict['zookeeper_myid']) + '=' + zookeeper_server + ':2888:3888' + '\n'
            basic_config['zookeeper_definition_list'] = zookeeper_definition_content

        mapping['zoo.cfg'] = replace_params(data, basic_config)

        ################## zookeeper-env.sh **********************************
        data = self.get_text_template('zookeeper-env.sh')
        mapping['zookeeper-env.sh'] = replace_params(data, basic_config)

        ################# log4j.properties ###########################
        data = self.get_text_template('log4j.properties')
        mapping['log4j.properties'] = replace_params(data, basic_config)

        return mapping

    def get_all_kv_from_config(self, group_name):
        return {}
