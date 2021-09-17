import requests
import base64
from services import Service

class GEMMAService(Service):
    usename = ""
    password = ""


    def __init__(self, username, password):
        self.usename = username
        self.password = password
    
    def prePareHeader(self):
        base64string = base64.encodestring(b'Wilson:chubbyt566').replace(b'\n', b"").decode('utf8')
        headers = {"Authorization" : f'Basic {base64string}'}
        return headers


    def returnServiceResults(self, gpl):
        super().returnServiceResults
        except NotImplementedError:
            url = f"https://gemma.msl.ubc.ca/rest/v2/datasets/{gpl}?offset=0&limit=20&sort=%2Bid"
            return requests.get(url, headers=self.prePareHeader).json()
    