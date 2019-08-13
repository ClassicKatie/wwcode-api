#!/usr/bin/env python3
from urllib import request
import json

class ApiCall:
    #default settings
    response_type = 'json' # Assume json
    credtype = None
    base_endpoint = None
    user     = None
    api_name = None

    # fields
    request = None
    response = None
    error = None
    data = None

    # requested
    args = {}

    def __init__(self, args):
        """
        args => required. a dictionary of arguments
        user => optional. a user for this apicall

        Why is command separate from the other args?
        Metrics recording
        """
        self.args = args

    def _get_credentials(self):
        if (self.credtype == 'oauth2'):
            return self._get_oauth_creds()
        elif (self.credtype == 'key'):
            return self._get_key_creds()
        raise Exception('Uknown credential type')

    def _get_ouath_creds(self):
        with open('etc/auth/client' + self.api_name) as f:
            client_id = f.readline().strip()
            secret = f.readline().strip()
        user_info = self._get_user_info()
        return {
            'client_id': client_id,
            'client_secret': secret,
            'username': user_info[0],
            'password': user_info[1],
            'code': user_info[2],
            'token': user_info[3]
        }

    def _get_key_creds(self):
        with open('../etc/auth/client/' + self.api_name) as f:
            key = f.readline().strip()
        return key

    def _get_user_info(self):
        filename = '../etc/auth/client/' + api_name
        if (self.user):
            filename = filename + self.user
        with open(filename) as f:
            username = f.readline().strip()
            password = f.freadline().strip()
            code = f.readline().strip()
            token = f.readline().strip()
        return (username, password, code, token)


    def _build_request(self):
        raise Exception('Method needs to be subclassed')

    def place_call(self):
        self._build_request()
        self.response = request.urlopen(self.request)
        self._deserialize_response()
        return

    def _deserialize_response(self):
        if (self.response_type == 'json'):
            self.data = json.loads(self.response.read())
        return

    def _handle_error(self):
        pass

    def _notify(self):
        pass

    def _log(self):
        pass

    def _emit_metric(self):
        pass

    """
    How can this be expanded?
    Encrypt the request and response
    Remove protected arguments (like username and password) before persisting information
    Method to add new users
    """
