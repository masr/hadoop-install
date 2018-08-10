from processor.abstract_process import AbstractProcess
from constants import SERVICE
from processor.utils import trans_dict_to_xml, replace_params


class HadoopProcess(AbstractProcess):
    def __init__(self, cluster_name, topology_data):
        AbstractProcess.__init__(self, cluster_name, SERVICE.HADOOP, topology_data
                                 , ['namenode', 'datanode', 'journal_node', 'zkfc', 'resource_manager', 'nodemanager'])

    def get_all_parsed_configs(self, group_name):
        params = self.get_merged_basic_configuration_by_group(group_name)
        mapping = {}
        data = self.get_merged_service_configuration_by_group('core-site.yaml', group_name)
        mapping['core-site.xml'] = trans_dict_to_xml(data, params)

        data = self.get_merged_service_configuration_by_group('hdfs-site.yaml', group_name)
        mapping['hdfs-site.xml'] = trans_dict_to_xml(data, params)

        data = self.get_text_template('hadoop-env.sh')
        mapping['hadoop-env.sh'] = replace_params(data, params)

        data = self.get_text_template('yarn-env.sh')
        mapping['yarn-env.sh'] = replace_params(data, params)

        return mapping
