#!/usr/bin/env python

__author__ = 'SLZ'

import time

import requests

from .base_handler import base_handler

class github_handler(base_handler):
    def __init__(self,config):
        base_handler.__init__(self, config)

    def redirect_to(self):
        return "https://github.com/login/oauth/authorize?scope=user&client_id=%s" % self.id
    
    def auth_from(self, received_params):
        code = received_params.get('code','')

        data={
            'client_id': self.id,
            'client_secret': self.secret,
            'code': code
        }

        headers = {'Accept': 'application/json'}
        r = requests.post(url = "https://github.com/login/oauth/access_token", data = data, headers= headers)
        json_data = r.json()

        token = json_data['access_token']
        auth_result = requests.get(url='https://api.github.com/user',params ={'access_token':token},headers=headers)
        auth_json_data = auth_result.json()
        auth_json_data['token'] = token
        auth_json_data['expires_at'] = int(time.time()+604800)

        email = auth_json_data['email']
        auth_data = self.create_auth_data(\
            auth_json_data['id'],\
            auth_json_data['expires_at'],\
            email,\
            auth_json_data['login'],\
            auth_json_data['avatar_url'],\
            self.name,\
            token,
            auth_json_data['html_url'])
        return auth_data