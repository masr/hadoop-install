from constants import SERVICE, ROLE
from processor.abstract_process import AbstractProcess
from processor.utils import replace_params, replace_values_in_dict, trans_dict_to_conf


class SparkProcess(AbstractProcess):
    def __init__(self, cluster_name, topology):
        AbstractProcess.__init__(self, cluster_name, SERVICE.SPARK, topology)

    def get_all_parsed_configs(self, group_name):
        mapping = self.parse_configs(group_name)
        mapping['spark-defaults.conf'] = trans_dict_to_conf(mapping['spark-defaults.conf'], ' ')
        return mapping

    def parse_configs(self, group_name):
        basic_config = self.get_merged_basic_configuration_by_group(group_name)
        spark_history_server = self.topology.get_hosts_of_role(ROLE.SPARKHISTORYSERVER)[0]
        basic_config['spark_history_server_vip'] = spark_history_server

        mapping = {}
        ################## spark-env.sh **********************************
        data = self.get_text_template('spark-env.sh')
        mapping['spark-env.sh'] = replace_params(data, basic_config)

        ################## log4j.properties **********************************
        data = self.get_text_template('log4j.properties')
        mapping['log4j.properties'] = replace_params(data, basic_config)

        ################# spark-defaults.conf ###########################
        data = self.get_merged_service_configuration_by_group('spark-defaults.yaml', group_name)
        mapping['spark-defaults.conf'] = replace_values_in_dict(data, basic_config)

        return mapping

    def get_all_kv_from_config(self, group_name):
        return {}
