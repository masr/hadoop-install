class ConfigGroup:
    def __init__(self, service_type, file_name, group_name, data):
        self.service_type = service_type
        self.file_name = file_name
        self.group_name = group_name
        if 'updates' in data and data['updates'] is not None:
            self.updates = data['updates']
        else:
            self.updates = {}
        if 'deletes' in data and data['deletes'] is not None:
            self.deletes = data['deletes']
        else:
            self.deletes = []
