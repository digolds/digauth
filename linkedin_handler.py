#!/usr/bin/env python

__author__ = 'SLZ'

import re, time

import requests

from .base_handler import base_handler

class linkedin_handler(base_handler):
    def __init__(self,config):
        base_handler.__init__(self, config)

    def redirect_to(self):
        return "https://www.linkedin.com/oauth/v2/authorization?client_id=%s&response_type=code&redirect_uri=%s&state=wakuangya" % (self.id,self.quote(self.auth_callback_url,safe=''))
    
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
        r = requests.post(url = "https://www.linkedin.com/oauth/v2/accessToken", data = data,headers=headers)
        token_data = r.json()
        params={}
        params['access_token']=token_data['access_token']
        params['expires_in']=int(time.time()+token_data['expires_in'])
        headers['Authorization'] = 'Bearer ' + params['access_token']
        r = requests.get(url='https://api.linkedin.com/v1/people/~:(id,first-name,picture-url,email-address,public-profile-url)?format=json',headers=headers)
        json_data = r.json()
        email = json_data['emailAddress']
        auth_data = self.create_auth_data(\
            json_data['id'],\
            params['expires_in'],\
            email,\
            json_data['firstName'],\
            'http://tvax3.sinaimg.cn/default/images/default_avatar_male_50.gif' if json_data.get('pictureUrl',None) is None else json_data['pictureUrl'],\
            self.name,\
            params['access_token'],\
            json_data['publicProfileUrl'])
        return auth_data
    
    def share_to(self, content_dict):
        share_content = content_dict.get('content')
        submitted_url = content_dict.get('submitted-url')
        image_url = content_dict.get('image_url')
        auth_token = content_dict.get('auth_token')
        data={
            "comment": share_content,
            "content": {
                "title": share_content,
                "description": share_content,
                "submitted-url": submitted_url,  
                "submitted-image-url": image_url
            },
            "visibility": {
                "code": "anyone"
            }
        }
        headers = {'Content-Type': 'application/json','x-li-format': 'json'}
        headers['Authorization'] = 'Bearer ' + auth_token
        r = requests.post(url = "https://api.linkedin.com/v1/people/~/shares?format=json", json = data, headers=headers)
        return r.json()