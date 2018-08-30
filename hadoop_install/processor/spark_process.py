from hadoop_install.constants import SERVICE, ROLE
from hadoop_install.processor.abstract_process import AbstractProcess
from hadoop_install.utils import replace_params, replace_values_in_dict, trans_dict_to_conf


class SparkProcess(AbstractProcess):
    def __init__(self, cluster_name, topology):
        AbstractProcess.__init__(self, cluster_name, SERVICE.SPARK, topology)

    def get_all_parsed_configs(self, group_name):
        mapping, basic_config = self.parse_configs(group_name)
        mapping['spark-defaults.conf'] = trans_dict_to_conf(mapping['spark-defaults.conf'], ' ')
        return mapping, basic_config

    def parse_configs(self, group_name):
        basic_config = self.get_merged_basic_configuration_by_group(group_name)
        mapping = {}

        if len(self.topology.get_hosts_of_role(ROLE.SPARKHISTORYSERVER)) != 0:
            spark_history_server = self.topology.get_hosts_of_role(ROLE.SPARKHISTORYSERVER)[0]
            if 'sparkhistoryserver1' not in basic_config:
                basic_config['sparkhistoryserver1'] = spark_history_server

        ################## spark-env.sh **********************************
        mapping['spark-env.sh'] = self.get_text_template('spark-env.sh')

        ################## log4j.properties **********************************
        mapping['log4j.properties'] = self.get_text_template('log4j.properties')

        ################# spark-defaults.conf ###########################
        mapping['spark-defaults.conf'] = self.get_merged_service_configuration_by_group('spark-defaults.yaml',
                                                                                        group_name)

        return mapping, basic_config

    def get_all_kv_from_config(self, group_name):
        return {}
