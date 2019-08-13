from apicall import ApiCall
from urllib import parse, request

class Nasa(ApiCall):
    api_name = 'nasa'
    credtype = 'key'
    base_endpoint = 'https://api.nasa.gov/'

    def __init__(self, args):
        self.args = args

    def _build_request(self):
        endpoint = self.base_endpoint + self.args['endpoint_postfix']
        content = self.args['params']
        content.update({'api_key': self._get_credentials()})
        parsed_content = parse.urlencode(content)
        url = ''.join([self.base_endpoint, self.args['endpoint_postfix'], parsed_content])
        self.request = request.Request(url)
        return

