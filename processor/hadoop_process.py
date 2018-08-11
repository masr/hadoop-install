from processor.abstract_process import AbstractProcess
from constants import SERVICE
from processor.utils import trans_dict_to_xml, replace_params, replace_values_in_dict


class HadoopProcess(AbstractProcess):
    def __init__(self, cluster_name, topology_data):
        AbstractProcess.__init__(self, cluster_name, SERVICE.HADOOP, topology_data
                                 , set(['namenode', 'datanode', 'journal_node'
                                           , 'zkfc', 'resource_manager', 'nodemanager']))

    def get_all_parsed_configs(self, group_name):
        mapping = self.parse_configs(group_name)

        ################## core-site.xml **********************************8
        mapping['core-site.xml'] = trans_dict_to_xml(mapping['core-site.xml'])

        ################## hdfs-site.xml **********************************
        mapping['hdfs-site.xml'] = trans_dict_to_xml(mapping['hdfs-site.xml'])

        ################## yarn-site.xml **********************************
        data = self.get_merged_service_configuration_by_group('yarn-site.yaml', group_name)
        mapping['yarn-site.xml'] = trans_dict_to_xml(mapping['yarn-site.xml'])

        return mapping

    def parse_configs(self, group_name):
        basic_config = self.get_merged_basic_configuration_by_group(group_name)

        zookeeper_servers = self.topology.get_hosts_of_role('zookeeper_server')
        zookeeper_config = self.get_other_service_configuration(SERVICE.ZOOKEEPER)
        zookeeper_port = zookeeper_config['zookeeper_server_port']
        zookeeper_quorum = ','.join([host + ':' + str(zookeeper_port) for host in zookeeper_servers])
        basic_config['zookeeper_quorum'] = zookeeper_quorum
        default_nameservice = basic_config['default_nameservice']
        namenodes = self.topology.get_hosts_of_role('namenode')
        basic_config['namenode1'] = namenodes[0]
        basic_config['namenode2'] = namenodes[1]
        resource_managers = self.topology.get_hosts_of_role('resource_manager')
        basic_config['resource_manager1'] = resource_managers[0]
        basic_config['resource_manager2'] = resource_managers[1]
        journal_nodes = self.topology.get_hosts_of_role('journal_node')
        qjournal_string = 'qjournal://' + ';'.join(
            [host + ':' + str(basic_config['journalnode_rpc_port']) for host in journal_nodes]
        ) + '/' + default_nameservice
        is_kerberos = basic_config['kerberos_enable']
        https_enable = basic_config['https_enable']
        if https_enable:
            basic_config['http_policy'] = 'HTTPS_ONLY'
        else:
            basic_config['http_policy'] = 'HTTP_ONLY'

        mapping = {}
        ################## core-site.xml **********************************8
        data = self.get_merged_service_configuration_by_group('core-site.yaml', group_name)
        mapping['core-site.xml'] = replace_values_in_dict(data, basic_config)

        ################## hdfs-site.xml **********************************
        data = self.get_merged_service_configuration_by_group('hdfs-site.yaml', group_name)

        data['dfs.namenode.shared.edits.dir'] = qjournal_string

        mapping['hdfs-site.xml'] = replace_values_in_dict(data, basic_config)

        ################## yarn-site.xml **********************************
        data = self.get_merged_service_configuration_by_group('yarn-site.yaml', group_name)
        mapping['yarn-site.xml'] = replace_values_in_dict(data, basic_config)

        ################## hadoop-env.sh **********************************
        data = self.get_text_template('hadoop-env.sh')
        mapping['hadoop-env.sh'] = replace_params(data, basic_config)

        ################## yarn-env.sh **********************************
        data = self.get_text_template('yarn-env.sh')
        mapping['yarn-env.sh'] = replace_params(data, basic_config)

        ################# log4j.properties ###########################
        data = self.get_text_template('log4j.properties')
        mapping['log4j.properties'] = replace_params(data, basic_config)

        return mapping

    def get_all_kv_from_config(self, group_name):
        mapping = self.parse_configs(group_name)
        result = mapping['core-site.xml'].copy()
        result.update(mapping['hdfs-site.xml'])
        result.update(mapping['yarn-site.xml'])

        if 'yarn.nodemanager.log-dirs' in result:
            result['yarn_nodemanager_log_dirs'] = result['yarn.nodemanager.log-dirs'].split(',')
        if 'yarn.nodemanager.local-dirs' in result:
            result['yarn_nodemanager_local_dirs'] = result['yarn.nodemanager.local-dirs'].split(',')
        if 'dfs.datanode.data.dir' in result:
            result['dfs_datanode_data_dir'] = result['dfs.datanode.data.dir'].split(',')
        if 'dfs.namenode.name.dir' in result:
            result['dfs_namenode_name_dir'] = result['dfs.namenode.name.dir'].split(',')

        return result
