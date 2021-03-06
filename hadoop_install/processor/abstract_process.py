import os

import yaml

from hadoop_install.constants import SERVICE_TO_ROLES
from hadoop_install.config_group import ConfigGroup
from hadoop_install.utils import check_and_create_dir, clean_and_create_dir, replace_values_in_dict, get_configuration


class AbstractProcess:

    def __init__(self, cluster_name, service_type, topology):
        self.cluster_name = cluster_name
        self.service_type = service_type
        self.service_name = service_type.value
        self.topology = topology
        self.config_group_names = topology.get_config_groups(service_type)

        self.cluster_base_dir = os.path.join('cluster', cluster_name)
        self.ansible_base_dir = os.path.join('cluster', cluster_name, '.ansible')
        self.confs_base_dir = os.path.join('cluster', cluster_name, '.confs')
        self.service_ansible_base_dir = os.path.join(self.ansible_base_dir, self.service_name)
        self.service_confs_base_dir = os.path.join(self.confs_base_dir, self.service_name)
        self.cluster_service_config_dir = os.path.join('cluster', cluster_name, 'config', self.service_name)
        self.hadoop_stack = self.get_hadoop_stack_name()
        self.common_dir = os.path.join('config', 'common')
        self.stack_dir = os.path.join('config', self.hadoop_stack)
        self.stack_service_config_dir = os.path.join('config', self.hadoop_stack, self.service_name)
        self.common_service_config_dir = os.path.join('config', 'common', self.service_name)

    def get_hadoop_stack_name(self):
        result = get_configuration(self.cluster_base_dir + "/config/configuration.yaml")
        if 'hadoop_stack' not in result:
            return "common"
        else:
            return result['hadoop_stack']

    def get_merged_basic_configuration_by_group(self, group_name):
        # /common/configuration.yaml
        result = get_configuration(self.common_dir + '/configuration.yaml')
        # /common/hadoop/configuration.yaml
        tmp_result = get_configuration(self.common_service_config_dir + '/configuration.yaml')
        result.update(tmp_result)
        if self.hadoop_stack != 'common':
            # /aws/configuration.yaml
            tmp_result = get_configuration(self.stack_dir + '/configuration.yaml')
            result.update(tmp_result)
            # /aws/hadoop/configuration.yaml
            tmp_result = get_configuration(self.stack_service_config_dir + '/configuration.yaml')
            result.update(tmp_result)
        # /cluster/amino/configuration.yaml
        tmp_result = get_configuration(self.cluster_base_dir + "/config/configuration.yaml")
        result.update(tmp_result)
        # /cluster/amino/config/hadoop/configuration.yaml
        tmp_result = get_configuration(self.cluster_service_config_dir + "/configuration.yaml")
        if 'default' in tmp_result:
            # /cluster/amino/config/hadoop/configuration.yaml#default
            result.update(tmp_result['default'])
        if group_name != 'default':
            if group_name in tmp_result:
                # /cluster/amino/config/hadoop/configuration.yaml#normal
                result.update(tmp_result[group_name])
        result = replace_values_in_dict(result, result)
        return result

    def get_merged_service_configuration_by_group(self, file_name, group_name):
        def merge_helper(group):
            if group in config_group_dict:
                group_result = config_group_dict[group].updates
                result.update(group_result)
                for delete in config_group_dict[group].deletes:
                    if delete in result:
                        del result[delete]

        # /common/hadoop/hdfs-site.xml
        result = get_configuration(self.common_service_config_dir + "/" + file_name)
        if self.hadoop_stack != 'common':
            # /aws/hadoop/hdfs-site.xml
            stack_result = get_configuration(self.stack_service_config_dir + "/" + file_name)
            result.update(stack_result)
        # /cluster/amino/config/hadoop/hdfs-site.xml
        config_group_dict = self.get_config_groups_of_a_file(file_name)
        # /cluster/amino/config/hadoop/hdfs-site.xml#default
        merge_helper('default')
        if group_name != 'default':
            # /cluster/amino/config/hadoop/hdfs-site.xml#normal
            merge_helper(group_name)
        return result

    def get_text_template(self, file_name):
        data = self.get_binary(file_name)
        if data is not None:
            return self.get_binary(file_name).decode("utf-8")
        else:
            return None

    def get_binary(self, file_name):
        result = None
        file_path = self.common_service_config_dir + "/" + file_name
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                result = file.read()
        if self.hadoop_stack != 'common':
            file_path = self.stack_service_config_dir + '/' + file_name
            if os.path.exists(file_path):
                with open(file_path, "rb") as file:
                    result = file.read()
        file_path = self.cluster_service_config_dir + "/" + file_name
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                result = file.read()
        return result

    def get_config_groups_of_a_file(self, file_name):
        config_detail_path = self.cluster_service_config_dir + "/" + file_name
        if not os.path.exists(config_detail_path):
            return {}
        else:
            config_group_dict = {}
            with open(config_detail_path) as config_group_file:
                data = yaml.load(config_group_file.read(), Loader=yaml.Loader)
                if data is None:
                    data = {}
                for group_name in data:
                    config_group = ConfigGroup(self.service_type, file_name, group_name, data[group_name])
                    config_group_dict[group_name] = config_group
            return config_group_dict

    def generate_configs(self):
        group_content_dict = {}
        for group_name in self.config_group_names:
            group_content_dict[group_name], _ = self.get_all_parsed_configs(group_name)
        check_and_create_dir(self.confs_base_dir)
        clean_and_create_dir(self.service_confs_base_dir)

        for group_name, content_dict in group_content_dict.items():
            target_path = self.service_confs_base_dir + "/" + group_name
            clean_and_create_dir(target_path)
            for file_name, content in content_dict.items():
                if type(content) == str:
                    with open(target_path + "/" + file_name, "w") as tmp_file:
                        tmp_file.write(content)
                else:
                    with open(target_path + "/" + file_name, "wb") as tmp_file:
                        tmp_file.write(content)

    def generate_ansible(self):
        check_and_create_dir(self.ansible_base_dir)
        clean_and_create_dir(self.service_ansible_base_dir)

        inventory_content = ""
        for role in SERVICE_TO_ROLES[self.service_type]:
            inventory_content += "[" + role.value + "]\n"
            inventory_content += "\n".join(self.topology.get_hosts_of_role(role)) + "\n\n"
        for group_name in self.config_group_names:
            inventory_content += "[" + group_name + "]\n"
            inventory_content += "\n".join(self.topology.get_hosts_of_group(self.service_type, group_name)) + "\n\n"
        with open(self.service_ansible_base_dir + "/hosts", "w") as tmp_file:
            tmp_file.write(inventory_content)

        includes = []
        clean_and_create_dir(self.service_ansible_base_dir + "/vars")
        for group_name in self.config_group_names:
            (_, basic_config) = self.get_all_parsed_configs(group_name)
            basic_config.update(self.get_all_kv_from_config(group_name))
            with open(self.service_ansible_base_dir + "/vars/" + group_name + ".yaml", "w") as tmp_file:
                basic_config[
                    'group_conf_dir'] = '../' + self.service_confs_base_dir + '/' + group_name
                basic_config['host_params'] = {}
                for host in self.topology.get_hosts_of_service(self.service_type):
                    basic_config['host_params'][host] = self.topology.get_vars_from_host(host)
                content = yaml.dump(basic_config, default_flow_style=False)
                tmp_file.write(content)
            includes.append(
                {
                    'name': 'install ' + self.service_name + ' for group ' + group_name,
                    'import_playbook': '../../../../playbooks/install_' + self.service_name + '.yaml',
                    'vars': {
                        'variable_hosts': group_name,
                        'config_group_name': group_name,
                        'vars_file': '../cluster/' + self.cluster_name + '/.ansible/' + self.service_name + '/vars/' + group_name + '.yaml'
                    }
                }
            )
        with open(self.service_ansible_base_dir + "/install.yaml", "w") as tmp_file:
            content = yaml.dump(includes, default_flow_style=False)
            tmp_file.write(content)

    def get_other_service_configuration(self, service_type):
        service_name = service_type.value
        result = get_configuration(self.common_dir + '/' + service_name + "/configuration.yaml")
        tmp_result = get_configuration(self.stack_dir + '/' + service_name + "/configuration.yaml")
        result.update(tmp_result)
        cluster_result = get_configuration(os.path.join(self.cluster_base_dir, service_name, "configuration.yaml"))
        if 'default' in cluster_result:
            result.update(cluster_result['default'])
        return result

    def get_all_parsed_configs(self, group_name):
        # Return type is tuple, the first ele is dict of different of config files, the second one is enhanced basic configuration.
        return {}, {}

    def get_all_kv_from_config(self, group_name):
        return {}
