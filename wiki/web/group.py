"""
    Group classes & helpers
    ~~~~~~~~~~~~~~~~~~~~~~
"""
import os
import json
import binascii
import hashlib
from functools import wraps

from flask import current_app


class GroupManager(object):
    """A very simple group Manager, that saves it's data as json."""
    def __init__(self, path):
        self.file = os.path.join(path, 'groups.json')

    def read(self):
        if not os.path.exists(self.file):
            return {}
        with open(self.file) as f:
            data = json.loads(f.read())
        return data

    def write(self, data):
        with open(self.file, 'w') as f:
            f.write(json.dumps(data, indent=2))

    def add_group(self, name, roles=[]):
        groups = self.read()
        if groups.get(name):
            return False

        new_group = {
            'roles': roles
        }
        groups[name] = new_group
        self.write(groups)
        groupdata = groups.get(name)
        return Group(self, name, groupdata)

    def get_groups(self):
        groups = self.read()
        group_objects = []
        print(groups)
        for key, value in groups.items():
            group_objects.append(Group(self, key, value))
            print(group_objects)
        if not group_objects:
            return None
        return group_objects

    def get_group(self, name):
        groups = self.read()
        groupdata = groups.get(name)
        if not groupdata:
            return None
        return Group(self, name, groupdata)

    def delete_group(self, name):
        groups = self.read()
        if not groups.pop(name, False):
            return False
        self.write(groups)
        return True

    def update(self, name, groupdata):
        data = self.read()
        data[name] = groupdata
        self.write(data)

    def index(self):
        groups = self.read()
        group_objects = []
        for group in groups.items():
            group_objects.append({"name": group[0], "url": "/group/" + group[0]})
        return group_objects


class Group(object):
    def __init__(self, manager, name, data):
        self.manager = manager
        self.name = name
        self.data = data

    def get(self, option):
        return self.data.get(option)

    def set(self, option, value):
        self.data[option] = value
        self.save()

    def save(self):
        self.manager.update(self.name, self.data)

    def get_id(self):
        return self.name
