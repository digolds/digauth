#!/usr/bin/env python

__author__ = 'SLZ'

from .weibo_handler import weibo_handler
from .github_handler import github_handler
from .linkedin_handler import linkedin_handler

auth_providers = []
config = {}


def make_config(name,id,secret,auth_callback_url):
    c = {}
    c['name'] = name
    c['id'] = id
    c['secret'] = secret
    c['auth_callback_url'] = auth_callback_url
    config[name] = c

def _create_handler_ins(name):
    if name == 'weibo':
        return weibo_handler(config[name])
    elif name == 'github':
        return github_handler(config[name])
    elif name == 'linkedin':
        return linkedin_handler(config[name])

def get_auth_handler(name):
    for i in auth_providers:
        if i.name == name:
            return i
    hd = _create_handler_ins(name)
    auth_providers.append(hd)
    return hd