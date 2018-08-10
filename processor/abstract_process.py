import yaml

from processor.config_group import ConfigGroup
from processor.utils import check_and_create_dir, clean_and_create_dir
from processor.topology import Topology
import os


class AbstractProcess:

    def __init__(self, cluster_name, service_type, topology_data, roles=set()):
        self.cluster_name = cluster_name
        self.service_type = service_type
        self.service_name = str(service_type.name).lower()
        self.topology_data = topology_data
        self.topology = Topology(topology_data)
        if 'config_groups' in topology_data and 'hadoop' in topology_data['config_groups']:
            self.config_group_names = set(topology_data['config_groups']['hadoop'])
        else:
            self.config_group_names = set()
        self.config_group_names.add("default")
        self.roles = roles

    def get_merged_basic_configuration_by_group(self, group_name):
        result = self.get_configuration("config/" + self.service_name + "/configuration.yaml")
        cluster_result = self.get_configuration(
            "cluster/" + self.cluster_name + "/config/" + self.service_name + "/configuration.yaml")
        if group_name in cluster_result:
            result.update(cluster_result[group_name])
        return result

    def get_merged_service_configuration_by_group(self, file_name, group_name):
        result = self.get_configuration("config/" + self.service_name + "/" + file_name)
        config_group_dict = self.get_cluster_config_details(file_name)
        if group_name in config_group_dict:
            if 'default' in config_group_dict:
                result.update(config_group_dict['default'].updates)
                for delete_key in config_group_dict['default'].deletes:
                    if delete_key in result:
                        del result[delete_key]
            config_group = config_group_dict[group_name]
            result.update(config_group.updates)
            for delete_key in config_group.deletes:
                if delete_key in result:
                    del result[delete_key]
        return result

    def get_configuration(self, config_file_path):
        result = {}
        if os.path.exists(config_file_path):
            with open(config_file_path) as config_file:
                result = yaml.load(config_file.read(), Loader=yaml.Loader)
        return result

    def get_text_template(self, file_name):
        result = None
        file_path1 = "config/" + self.service_name + "/" + file_name
        if os.path.exists(file_path1):
            with open(file_path1) as file1:
                result = file1.read()
        file_path2 = "cluster/" + self.cluster_name + "/config/" + self.service_name + "/" + file_name
        if os.path.exists(file_path2):
            with open(file_path2) as file2:
                result = file2.read()
        return result

    def get_cluster_config_details(self, file_name):
        config_detail_path = "cluster/" + self.cluster_name + "/config/" + self.service_name + "/" + file_name
        if not os.path.exists(config_detail_path):
            return {}
        else:
            config_group_dict = {}
            with open(config_detail_path) as config_group_file:
                data = yaml.load(config_group_file.read(), Loader=yaml.Loader)
                for group_name in data:
                    self.config_group_names.add(group_name)
                    config_group = ConfigGroup(self.service_type, file_name, group_name, data[group_name])
                    config_group_dict[group_name] = config_group
            return config_group_dict

    def generate_configs(self):
        group_content_dict = {}
        for group_name in self.config_group_names:
            group_content_dict[group_name] = self.get_all_parsed_configs(group_name)
        tmp_path = "cluster/" + self.cluster_name + "/.confs"
        check_and_create_dir(tmp_path)
        clean_and_create_dir(tmp_path + "/" + self.service_name)
        target_path = tmp_path + "/" + self.service_name + "/" + group_name
        clean_and_create_dir(target_path)
        for group_name, content_dict in group_content_dict.items():
            for file_name, content in content_dict.items():
                with open(target_path + "/" + file_name, "w") as tmp_file:
                    tmp_file.write(content)

    def generate_ansible(self):
        tmp_path = "cluster/" + self.cluster_name + "/.ansible"
        check_and_create_dir(tmp_path)
        target_path = tmp_path + '/' + self.service_name
        clean_and_create_dir(target_path)

        inventory_content = ""
        for role in self.roles:
            inventory_content += "[" + role + "]\n"
            inventory_content += "\n".join(self.topology.get_hosts_of_role(role)) + "\n\n"
        for group_name in self.config_group_names:
            inventory_content += "[" + group_name + "]\n"
            inventory_content += "\n".join(self.topology.get_hosts_of_group(self.service_type, group_name)) + "\n\n"
        with open(target_path + "/hosts", "w") as tmp_file:
            tmp_file.write(inventory_content)

        includes = []
        clean_and_create_dir(target_path + "/vars")
        for group_name in self.config_group_names:
            params = self.get_merged_basic_configuration_by_group(group_name)
            with open(target_path + "/vars/" + group_name + ".yaml", "w") as tmp_file:
                content = yaml.dump(params, default_flow_style=False)
                tmp_file.write(content)
            includes.append({'include': '../../../../playbooks/install_' + self.service_name + '.yaml',
                             'vars': {'variable_hosts': group_name}})
        with open(target_path + "/install.yaml", "w") as tmp_file:
            content = yaml.dump(includes, default_flow_style=False)
            tmp_file.write(content)

    def get_all_parsed_configs(self, group_name):
        return {}
