from hadoop_install.constants import SERVICE
from hadoop_install.processor.abstract_process import AbstractProcess


class NilProcess(AbstractProcess):
    def __init__(self, cluster_name, topology):
        AbstractProcess.__init__(self, cluster_name, SERVICE.NIL, topology)

    def get_all_parsed_configs(self, group_name):
        return {}, self.get_merged_basic_configuration_by_group(group_name)