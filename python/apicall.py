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
        """
        self.args = args

    def _get_credentials(self):
        if (self.credtype == 'oauth2'):
            return self._get_oauth_creds()
        elif (self.credtype == 'key'):
            return self._get_key_creds()
        raise Exception('Uknown credential type')

    def _get_oauth_creds(self):
        oauth_creds = self._get_client_info()
        user_info = self._get_user_info()
        oauth_creds.update({'access_token': user_info})
        return oauth_creds

    def _get_key_creds(self):
        with open('../etc/auth/client/' + self.api_name) as f:
            key = f.readline().strip()
        return key

    def _get_client_info(self):
        with open('../etc/auth/client/' + self.api_name) as f:
            client_id = f.readline().strip()
            secret = f.readline().strip()
        return {'client_id': client_id, 'secret': secret}

    def _get_user_info(self):
        filename = '../etc/auth/user/' + self.api_name
        if (self.user):
            filename = filename + '/' + self.user
        with open(filename) as f:
            code = f.readline().strip()
        return code

    def _build_request(self):
        raise Exception('Method needs to be subclassed')

    def place_call(self):
        self._build_request()
        self.response = request.urlopen(self.request)
        print(self.response)
        if self.call_successful():
            self._deserialize_response()
        else:
            self._handle_error()
        self._log()
        return

    def call_successful(self):
        """
        NB: This does not mean that you didn't get back an error!  You very
        well could have.  What it means is that you got back a real response
        from the api.  Which may or may not contain an error
        """
        successful_codes = [200, 201, 202, 203, 204, 205, 206, 207, 208, 226]
        print(self.response.status)
        if (self.response.status in successful_codes):
            return True
        else:
            return False

    def _deserialize_response(self):
        if (self.response_type == 'json'):
            self.data = json.loads(self.response.read())
            if not self.data:
                self.error = 'Did not get expected format for response'
        return

    def _handle_error(self):
        """
        Call errors are going to be stored in different places depending on the api
        you are using.  This method will likely need to be subclassed
        """
        if not self.data:
            print("No data in response")
            self.error = 'No data in response'
            self._notify()

    def _notify(self):
        pass

    def _log(self):
        # Why have something different for logging and metric emissions?
        # Sometimes this is going to be a matter of security, technology or
        # teams It also lets us separate out the different uses, so each does
        # its purpose well instead of trying to do everything.
        pass

    """
    How can this be expanded?
    Encrypt the request and response
    Remove protected arguments (like username and password) before persisting information
    Method to add new users
    """
