#!/usr/bin/env python

__author__ = 'SLZ'

import urllib

class base_handler(object):
    def __init__(self, args_dict):
        self.name = args_dict.get('name')
        self.id = args_dict.get('id')
        self.secret = args_dict.get('secret')
        self.auth_callback_url = args_dict.get('auth_callback_url')
    
    def redirect_to(self):
        pass
    
    def auth_from(self, received_params):
        pass
    
    def share_to(self, content_dict):
        pass
    
    def quote(self, s, encoding='utf-8',safe='/'):
        return urllib.parse.quote(s.encode(encoding),safe)
    
    def create_auth_data(self, id,expires_at,email,login,avatar_url,provider,token,url):
        d = {
            'id': str(id),
            'expires_at': expires_at,
            'email' : email,
            'login' : login,
            'avatar_url' : avatar_url,
            'provider' : provider,
            'token' : token,
            'url' : url
            }
        return d