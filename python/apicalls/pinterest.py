#!/usr/bin/env python3

from apicall import ApiCall
from urllib import parse,request

class Pinterest(ApiCall):
    response_type = None
    api_name = 'pinterest'
    credtype = 'oauth2'
    base_endpoint = 'https://api.pinterest.com/'

    def __init__(self, user, args):
        self.args = args
        self.user = user

    def _build_request(self):
        # Note that these api examples are mostly focused on GET requests, not post requests
        request_type = self.args['request_type']
        if request_type == 'GET':
            return self._build_GET_request()
        elif request_type == 'POST':
            return self._build_POST_request()
        else:
            raise Exception("not a valid request type")
        return;

    def _build_GET_request(self):
        url = self.base_endpoint + self.args['endpoint_postfix'] + '?'
        creds = self._get_credentials()
        params = {
            'access_token': creds['access_token'],
            'fields': ','.join(self.args['params']['fields'])
        }
        parsed_params = parse.urlencode(params)
        print(url)
        print(parsed_params)
        self.request = request.Request(url + parsed_params)

        return

    def _build_POST_request(self):
        #TODO
        pass

    def user_auth_link(self):
        # This is used to get a client token
        endpoint = 'https://api.pinterest.com/oauth/?'
        client_info = self._get_client_info()
        params = {
            'scope':'read_public,write_public',
            'state': 'a1b2c3d4',
            'client_id': client_info['client_id'],
            'response_type': 'code',
            'redirect_uri': 'https://katieford.io',
            }
        parsed = parse.urlencode(params)
        print(endpoint + parsed)
        return
