from hadoop_install.constants import SERVICE_TO_ROLES, SERVICE


class Topology:
    def __init__(self, topology_data):
        self.topology_data = topology_data
        self.inventory_hosts = topology_data['inventory']

    def get_hosts_of_role(self, role):
        hosts = []
        for host in self.inventory_hosts:
            data = self.inventory_hosts[host]
            if 'roles' in data:
                if role.value in data['roles']:
                    hosts.append(host)
        return sorted(hosts)

    def get_hosts_of_group(self, service_type, group_name):
        hosts = []
        service_name = service_type.value
        service_hosts = self.get_hosts_of_service(service_type)
        inventory_hosts = set(service_hosts) & set(self.inventory_hosts.keys())
        for host in inventory_hosts:
            data = self.inventory_hosts[host]
            if 'config_groups' in data:
                if service_name in data['config_groups']:
                    if group_name == data['config_groups'][service_name]:
                        hosts.append(host)
                else:
                    if group_name == 'default':
                        hosts.append(host)
            else:
                if group_name == 'default':
                    hosts.append(host)
        return sorted(hosts)

    def get_hosts_of_service(self, service_type):
        if service_type == SERVICE.JAVA:
            return sorted(self.inventory_hosts.keys())

        roles = SERVICE_TO_ROLES[service_type]
        host_set = set()
        for role in roles:
            host_set = host_set | set(self.get_hosts_of_role(role))
        return sorted(list(host_set))

    def get_vars_from_host(self, host):
        result = {}
        if host in self.inventory_hosts:
            host_inventory = self.inventory_hosts[host]
            if 'vars' in host_inventory:
                result = host_inventory['vars']
        return result

    def get_all_hosts(self):
        return self.inventory_hosts.keys()

    def get_config_groups(self, service_type):
        service_name = service_type.value
        result = set(['default'])
        for host in self.inventory_hosts:
            host_inventory = self.inventory_hosts[host]
            if 'config_groups' in host_inventory:
                if service_name in host_inventory['config_groups']:
                    result.add(host_inventory['config_groups'][service_name])
        return list(result)
