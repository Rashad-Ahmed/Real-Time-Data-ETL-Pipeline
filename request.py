import  requests
from auth import headers
import json

class Request:
    def __init__(self):
        self._header = headers

    @staticmethod
    def get_content(url, param):
        response = requests.get(url, headers=headers, params=param)
        if response.status_code == 200:
            return json.loads(response.content)
        else:
            print("Request completed with Error. Response Code : {}".format(response.status_code))
            return None