#!/usr/bin/env python

__author__ = 'SLZ'

import re, time

import requests

from .base_handler import base_handler

class weibo_handler(base_handler):
    def __init__(self,config):
        base_handler.__init__(self, config)

    def redirect_to(self):
        return "https://api.weibo.com/oauth2/authorize?client_id=%s&response_type=code&redirect_uri=%s" % (self.id,self.quote(self.auth_callback_url,safe=''))
    
    def auth_from(self, received_params):
        code = received_params.get('code','')

        data={
            'client_id': self.id,
            'client_secret': self.secret,
            'code': code
        }

        headers = {'Accept': 'application/json'}
        data['grant_type'] = 'authorization_code'
        data['redirect_uri']= self.auth_callback_url
        r = requests.post(url = "https://api.weibo.com/oauth2/access_token", data = data,headers=headers)
        token_data = r.json()

        params={}
        params['access_token']=token_data['access_token']
        params['uid']=token_data['uid']
        r = requests.get(url='https://api.weibo.com/2/users/show.json',params=params)
        json_data = r.json()

        email = received_params.get('email','')
        auth_data = self.create_auth_data(\
        json_data['id'],\
        int(time.time()+token_data['expires_in']),\
        email,\
        json_data['screen_name'],\
        json_data['profile_image_url'],\
        self.name,\
        token_data['access_token'],
        'https://weibo.com/'+json_data['profile_url'])
        return auth_data
    
    def share_to(self, content_dict):
        share_content = content_dict.get('content')
        submitted_url = content_dict.get('submitted-url')
        data={
            'access_token': content_dict.get('auth_token'),
            'status': share_content + ',' + submitted_url
        }
        headers = {'Accept': 'application/json'}
        r = None
        image_url = content_dict.get('image_url')
        if image_url:
            response = requests.get(image_url)
            files = {}
            files['pic'] = response.content
            r = requests.post(url = "https://api.weibo.com/2/statuses/share.json",data = data, files = files, headers=headers)
        else:
            r = requests.post(url = "https://api.weibo.com/2/statuses/share.json", data = data,headers=headers)
        return r.json()