import json
import pickle

class Credentials:
    def __init__(self, username, password, domain):
        self.username = username
        self.password = password
        self.domain = domain

class MountPoint:
    def __init__(self, name, size):
        self.name = name
        self.size = size

class Source:
    def __init__(self, ip, credentials, mount_points):
        if ip is None or credentials is None or any([mp is None for mp in mount_points]):
            raise ValueError('IP, credentials, and mount_points cannot be None')
        self.ip = ip
        self.credentials = credentials
        self.mount_points = mount_points

class MigrationTarget:
    VALID_CLOUD_TYPES = {'aws', 'azure', 'vsphere', 'vcloud'}

    def __init__(self, cloud_type, credentials, vm):
        if cloud_type not in self.VALID_CLOUD_TYPES or credentials is None or vm is None:
            raise ValueError('Invalid cloud_type, credentials, or vm')
        self.cloud_type = cloud_type
        self.credentials = credentials
        self.vm = vm

class Migration:
    STATE_NOT_STARTED = 'not started'
    STATE_RUNNING = 'running'
    STATE_ERROR = 'error'
    STATE_SUCCESSFUL = 'successful'

    def __init__(self, mount_points, source, target):
        if any([mp not in source.mount_points for mp in mount_points]):
            raise ValueError('Selected mount points must be in source mount points')
        self.mount_points = mount_points
        self.source = source
        self.target = target
        self.state = self.STATE_NOT_STARTED

    def run(self):
        if 'C:\\' not in self.mount_points:
            raise ValueError('C:\\ mount point is required')

        # Simulate migration for X minutes
        self.state = self.STATE_RUNNING
        # Copy source to target
        # Limit target mount points to selected ones
        self.state = self.STATE_SUCCESSFUL


class FileStorage:
    def __init__(self, file_path):
        self.file_path = file_path

    def create(self, obj):
        with open(self.file_path, 'a') as f:
            json.dump(obj.__dict__, f)
            f.write('\n')

    def update(self, obj):
        new_objs = []
        with open(self.file_path, 'r') as f:
            for line in f:
                obj_dict = json.loads(line)
                if obj_dict.get('ip') == obj.ip:
                    new_objs.append(obj.__dict__)
                else:
                    new_objs.append(obj_dict)

        with open(self.file_path, 'w') as f:
            for obj_dict in new_objs:
                json.dump(obj_dict, f)
                f.write('\n')

    def read(self, ip):
        with open(self.file_path, 'r') as f:
            for line in f:
                obj_dict = json.loads(line)
                if obj_dict.get('ip') == ip:
                    return Source(**obj_dict)

    def delete(self, ip):
        new_objs = []
        with open(self.file_path, 'r') as f:
            for line in f:
                obj_dict = json.loads(line)
                if obj_dict.get('ip') != ip:
                    new_objs.append(obj_dict)

        with open(self.file_path, 'w') as f:
            for obj_dict in new_objs:
                json.dump(obj_dict, f)
                f.write('\n')
