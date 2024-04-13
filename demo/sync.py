# encoding: utf-8
import uuid
import time
import requests
#import pymysql
from auth_util import gen_sign_headers

# Please replace APP_ID, APP_KEY
APP_ID = '3034578807'
APP_KEY = 'fBPijlvBzBXzjbae'
URI = '/vivogpt/completions'
DOMAIN = 'api-ai.vivo.com.cn'
METHOD = 'POST'


def sync_vivogpt(prompt):
    params = {
        'requestId': str(uuid.uuid4())
    }
    print('requestId:', params['requestId'])

    data = {
        'prompt': prompt,  # Modify this line to accept user input
        'model': 'vivo-BlueLM-TB',
        'sessionId': str(uuid.uuid4()),
        'extra': {
            'temperature': 0.9
        }
    }
    headers = gen_sign_headers(APP_ID, APP_KEY, METHOD, URI, params)
    headers['Content-Type'] = 'application/json'

    start_time = time.time()
    url = 'https://{}{}'.format(DOMAIN, URI)
    response = requests.post(url, json=data, headers=headers, params=params, stream=True)

    if response.status_code == 200:
        res_obj = response.json()
        print(f'response:{res_obj}')
        if res_obj['code'] == 0 and res_obj.get('data'):
            content = res_obj['data']['content']
            print(f'final content:\n{content}')
    else:
        print(response.status_code, response.text)
    end_time = time.time()
    timecost = end_time - start_time
    print('请求耗时: %.2f秒' % timecost)


if __name__ == '__main__':
    # Get user input for the prompt
    while(1):
        user_prompt = input(">>>Enter your prompt for the poem >>>")
        sync_vivogpt(user_prompt)


