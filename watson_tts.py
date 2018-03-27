import requests
import json
from requests.auth import HTTPBasicAuth

URL = 'https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize'
data = {'text': 'hello world hello world'}
HEADERS = {'content-type': 'application/json'}
AUTH = HTTPBasicAuth('250359ae-5159-4534-b885-65a21eccfa39', '6Pj5tlsZfrSx')

def watson_tts(file, text):
    data = json.dumps({'text': text})
    response = requests.post(URL, data=data, headers=HEADERS, auth=AUTH)
    f = open(file, 'wb')
    f.write(response.content)
    f.close()

if __name__ == '__main__':
    watson_tts('out.ogg', 'hello world')
