class Topology:
    def __init__(self, topology_data):
        self.topology_data = topology_data
        self.inventory_hosts = topology_data['inventory']

    def get_hosts_of_role(self, role_name):
        hosts = []
        for host in self.inventory_hosts:
            data = self.inventory_hosts[host]
            if 'roles' in data:
                if role_name in data['roles']:
                    hosts.append(host)
        return hosts

    def get_hosts_of_group(self, service_type, group_name):
        hosts = []
        service_name = str(service_type.name).lower()
        for host in self.inventory_hosts:
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
        return hosts
