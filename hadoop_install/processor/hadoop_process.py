from hadoop_install.constants import SERVICE, ROLE
from hadoop_install.processor.abstract_process import AbstractProcess
from hadoop_install.utils import trans_dict_to_xml, delete_keys_by_prefix


class HadoopProcess(AbstractProcess):
    def __init__(self, cluster_name, topology):
        AbstractProcess.__init__(self, cluster_name, SERVICE.HADOOP, topology)

    def get_all_parsed_configs(self, group_name):
        mapping, basic_config = self.parse_configs(group_name)

        for i in ['core-site.xml', 'hdfs-site.xml', 'yarn-site.xml', 'mapred-site.xml', 'capacity-scheduler.xml']:
            if i in mapping:
                mapping[i] = trans_dict_to_xml(mapping[i])
        return mapping, basic_config

    def parse_configs(self, group_name):
        basic_config = self.get_merged_basic_configuration_by_group(group_name)

        default_nameservice = basic_config['default_nameservice']

        https_enable = basic_config['https_enable']
        if https_enable == "true":
            basic_config['http_policy'] = 'HTTPS_ONLY'
        else:
            basic_config['http_policy'] = 'HTTP_ONLY'

        if len(self.topology.get_hosts_of_role(ROLE.ZOOKEEPER)) != 0:
            zookeepers = self.topology.get_hosts_of_role(ROLE.ZOOKEEPER)
            zookeeper_config = self.get_other_service_configuration(SERVICE.ZOOKEEPER)
            zookeeper_port = zookeeper_config['zookeeper_port']
            zookeeper_quorum = ','.join([host + ':' + str(zookeeper_port) for host in zookeepers])
            basic_config['zookeeper_quorum'] = zookeeper_quorum
        else:
            basic_config['zookeeper_quorum'] = ""

        if len(self.topology.get_hosts_of_role(ROLE.NAMENODE)) != 0:
            has_hdfs = True
            journalnodes = self.topology.get_hosts_of_role(ROLE.JOURNALNODE)
            basic_config['qjournal_quorum'] = 'qjournal://' + ';'.join(
                [host + ':' + str(basic_config['journalnode_rpc_port']) for host in journalnodes]
            ) + '/' + default_nameservice
        else:
            basic_config['qjournal_quorum'] = ""
            has_hdfs = False

        resourcemanagers = self.topology.get_hosts_of_role(ROLE.RESOURCEMANAGER)
        if len(resourcemanagers) != 0:
            has_yarn = True
            if len(resourcemanagers) == 1:
                if 'resourcemanager1' not in basic_config:
                    basic_config['resourcemanager1'] = resourcemanagers[0]
        else:
            has_yarn = False

        jobhistoryservers = self.topology.get_hosts_of_role(ROLE.JOBHISTORYSERVER)
        if len(jobhistoryservers) != 0:
            has_jobhistoryserver = True
            if 'jobhistoryserver1' not in basic_config:
                basic_config['jobhistoryserver1'] = jobhistoryservers[0]
        else:
            has_jobhistoryserver = False

        mapping = {}
        mapping['hdfs-site.xml'] = {}
        mapping['yarn-site.xml'] = {}
        mapping['mapred-site.xml'] = {}

        ################## core-site.xml **********************************
        mapping['core-site.xml'] = self.get_merged_service_configuration_by_group('core-site.yaml', group_name)

        if has_hdfs:
            ################## hdfs-site.xml **********************************
            data = self.get_merged_service_configuration_by_group('hdfs-site.yaml', group_name)
            data['dfs.namenode.name.dir'] = ','.join(basic_config['dfs_namenode_name_dir'])
            data['dfs.datanode.data.dir'] = ','.join(basic_config['dfs_datanode_data_dir'])
            mapping['hdfs-site.xml'] = data
            ################ hdfs-include ####################################
            mapping['hdfs-include'] = '\n'.join(self.topology.get_hosts_of_role(ROLE.DATANODE))

        if has_yarn:
            ################## yarn-site.xml #################################
            data = self.get_merged_service_configuration_by_group('yarn-site.yaml', group_name)
            data['yarn.nodemanager.log-dirs'] = ','.join(basic_config['yarn_nodemanager_log_dirs'])
            data['yarn.nodemanager.local-dirs'] = ','.join(basic_config['yarn_nodemanager_local_dirs'])
            mapping['yarn-site.xml'] = data

            ################ yarn-include ####################################
            mapping['yarn-include'] = '\n'.join(self.topology.get_hosts_of_role(ROLE.NODEMANAGER))
            if not has_hdfs:
                ################## hdfs-site.xml #################################
                if mapping['yarn-site.xml']['yarn.log-aggregation-enable'] == 'true':
                    mapping['hdfs-site.xml'] = self.get_merged_service_configuration_by_group('hdfs-site.yaml',
                                                                                              group_name)

        if has_jobhistoryserver:
            ################## mapred-site.xml #################################
            mapping['mapred-site.xml'] = self.get_merged_service_configuration_by_group('mapred-site.yaml', group_name)
            if not has_yarn:
                ################# yarn-site.xml ###################################
                data = self.get_merged_service_configuration_by_group('yarn-site.yaml', group_name)
                data = delete_keys_by_prefix(data, "yarn.resourcemanager")
                mapping['yarn-site.xml'] = data

        ################## capacity-scheduler.xml #################################
        mapping['capacity-scheduler.xml'] = self.get_merged_service_configuration_by_group('capacity-scheduler.yaml',
                                                                                           group_name)

        ################## hadoop-env.sh **********************************
        mapping['hadoop-env.sh'] = self.get_text_template('hadoop-env.sh')

        ################## yarn-env.sh **********************************
        mapping['yarn-env.sh'] = self.get_text_template('yarn-env.sh')

        ################## mapred-env.sh **********************************
        mapping['mapred-env.sh'] = self.get_text_template('mapred-env.sh')

        ################# log4j.properties ###########################
        mapping['log4j.properties'] = self.get_text_template('log4j.properties')

        ################# container-executor.cfg ###########################
        mapping['container-executor.cfg'] = self.get_text_template('container-executor.cfg')

        ################ topology.py ###########################
        mapping['topology.py'] = self.get_text_template('topology.py')

        return mapping, basic_config

    def get_all_kv_from_config(self, group_name):
        return {}
