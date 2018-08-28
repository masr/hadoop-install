from hadoop_install.constants import SERVICE, ROLE
from hadoop_install.processor.abstract_process import AbstractProcess
from hadoop_install.utils import replace_params, replace_values_in_dict, trans_dict_to_xml


class HiveProcess(AbstractProcess):
    def __init__(self, cluster_name, topology):
        AbstractProcess.__init__(self, cluster_name, SERVICE.HIVE, topology)

    def get_all_parsed_configs(self, group_name):
        mapping = self.parse_configs(group_name)
        mapping['hive-site.xml'] = trans_dict_to_xml(mapping['hive-site.xml'])
        return mapping

    def parse_configs(self, group_name):
        basic_config = self.get_merged_basic_configuration_by_group(group_name)
        mapping = {}

        hivemetastores = self.topology.get_hosts_of_role(ROLE.HIVEMETASTORE)
        if len(hivemetastores) != 0:
            basic_config['hive_metastore_uris'] = ','.join(["thrift://" + h for h in hivemetastores])

        ################## hive-env.sh **********************************
        data = self.get_text_template('hive-env.sh')
        mapping['hive-env.sh'] = replace_params(data, basic_config)

        ################## log4j.properties **********************************
        data = self.get_text_template('log4j.properties')
        mapping['log4j.properties'] = replace_params(data, basic_config)

        ################# hive-site.xml ###########################
        data = self.get_merged_service_configuration_by_group('hive-site.yaml', group_name)
        mapping['hive-site.xml'] = replace_values_in_dict(data, basic_config)

        ################# hive.jceks ############################
        mapping['hive.jceks'] = self.get_binary('hive.jceks')
        return mapping

    def get_all_kv_from_config(self, group_name):
        return {}
