#!/usr/bin/env python

__author__ = 'SLZ'

import re, time

import requests

from .base_handler import base_handler

class linkedin_handler(base_handler):
    def __init__(self,config):
        base_handler.__init__(self, config)

    def redirect_to(self):
        return "https://www.linkedin.com/oauth/v2/authorization?client_id=%s&response_type=code&redirect_uri=%s&state=wakuangya&scope=%s" % (self.id,self.quote(self.auth_callback_url,safe=''),self.quote("r_liteprofile r_emailaddress w_member_social",safe=''))
    
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
        r = requests.get(url='https://api.linkedin.com/v2/me?projection=(id,firstName,lastName,profilePicture(displayImage~:playableStreams))',headers=headers)
        json_data = r.json()
        linkedId = json_data['id']
        firstNameDict = json_data['firstName']
        country = firstNameDict['preferredLocale']['country']
        language = firstNameDict['preferredLocale']['language']
        firstName = firstNameDict['localized'][language + '_' + country]
        image_url = 'http://tvax3.sinaimg.cn/default/images/default_avatar_male_50.gif' if json_data.get('profilePicture',None) is None else json_data['profilePicture']['displayImage~']['elements'][0]['identifiers'][0]['identifier']
        
        r = requests.get(url='https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))',headers=headers)
        json_data = r.json()
        email = json_data['elements'][0]['handle~']['emailAddress']
        auth_data = self.create_auth_data(\
            linkedId,\
            params['expires_in'],\
            email,\
            firstName,\
            image_url,\
            self.name,\
            params['access_token'],\
            '')
        return auth_data
    
    def share_to(self, content_dict):
        share_content = content_dict.get('content')
        submitted_url = content_dict.get('submitted-url')
        auth_token = content_dict.get('auth_token')
        data = {
    "author": 'urn:li:person:' + content_dict.get("auth_id"),
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": share_content
            },
            "shareMediaCategory": "ARTICLE",
            "media": [
                {
                    "status": "READY",
                    "description": {
                        "text": share_content
                    },
                    "originalUrl": submitted_url,
                    "title": {
                        "text": share_content
                    }
                }
            ]
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
}
        headers = {'Content-Type': 'application/json','x-li-format': 'json'}
        headers['Authorization'] = 'Bearer ' + auth_token
        headers['X-Restli-Protocol-Version'] = '2.0.0'
        r = requests.post(url = "https://api.linkedin.com/v2/ugcPosts", json = data, headers=headers)
        return r.json()