from processor.abstract_process import AbstractProcess
from constants import SERVICE
from processor.utils import trans_dict_to_xml, replace_params


class JavaProcess(AbstractProcess):
    def __init__(self, cluster_name, topology):
        AbstractProcess.__init__(self, cluster_name, SERVICE.JAVA, topology)

