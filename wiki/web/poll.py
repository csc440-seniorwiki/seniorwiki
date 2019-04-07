import os
import json
import binascii
import hashlib
from functools import wraps

from flask import current_app

class PollManager(object):
    """A very simple poll manager that saves its data as json."""
    def __init__(self, path):
        self.file = os.path.join(path, 'polls.json')

    def read(self):
        print("JSON path:")
        print(self.file)
        if not os.path.exists(self.file):
            return {}
        with open(self.file) as f:
            data = json.loads(f.read())
        return data

    def write(self, data):
        with open(self.file, 'w') as f:
            f.write(json.dumps(data, indent=2))

    def add_poll(self, name, title, options = [], votes = []):
        polls = self.read()
        if polls.get(name):
            return False
        new_poll = {
            'title': title,
            'options': options,
            'votes': votes
        }
        polls[name] = new_poll
        self.write(polls)
        polldata = polls.get(name)
        return Poll(self, name, polldata)

    def get_poll(self, name):
        polls = self.read()
        polldata = polls.get(name)
        if not polldata:
            return None
        return Poll(self, name, polldata)

    def delete_poll(self, name):
        polls = self.read()
        if not polls.pop(name, False):
            return False
        self.write(polls)
        return True

    def update(self, name, polldata):
        data = self.read()
        data[name] = polldata
        self.write(data)

    def get_basic_data(self, name):
        polls = self.read()
        polldata = polls.get(name)
        if not polldata:
            return None
        return Poll(self, name, polldata)


class Poll(object):
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

class PollBasic(object):
    def __init__(self, name, title):
        self.name = name
        self.title = title