class ConfigGroup:
    def __init__(self, service_type, file_name, group_name, data):
        self.service_type = service_type
        self.file_name = file_name
        self.group_name = group_name
        self.updates = data
