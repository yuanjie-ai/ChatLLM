#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : hunyuan
# @Time         : 2023/10/9 13:29
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os
# -*- coding: utf-8 -*-
# 运行环境python3
# 如果使用出错请注意sse版本是否正确, pip3 install sseclient-py==1.7.2
import time
import uuid
import json
import base64
import hashlib
import hmac
import requests
import sseclient
from chatllm.schemas.openai_api_protocol import *

_SIGN_HOST = "hunyuan.cloud.tencent.com"
_SIGN_PATH = "hyllm/v1/chat/completions"
_URL = "https://hunyuan.cloud.tencent.com/hyllm/v1/chat/completions"


def chat(appid, secretid, secretkey, messages):
    request = gen_param(appid, messages, secretid, 0)
    signature = gen_signature(secretkey, gen_sign_params(request))
    # print(signature)
    headers = {
        "Content-Type": "application/json",
        "Authorization": str(signature)
    }
    print('Input:\n{} | {} | {}'.format(_URL, headers, request))

    url = _URL
    resp = requests.post(url, headers=headers, json=request, stream=True)
    print('Output:')
    output_str = ""
    data_js = resp.json()
    if 'error' in data_js:
        print(data_js['error']['message'])
    else:
        output_str = data_js['choices'][0]['messages']['content']
        print(data_js['choices'][0]['messages']['content'], end='', flush=True)
    return output_str


def chat_stream(appid, secretid, secretkey, messages):
    """
    {
        "req_id": "5803e3ca-a000-46e6-abb1-f98a775db161",
        "note": "以上内容为AI生成，不代表开发者立场，请勿删除或修改本标记",
        "choices": [
            {
                "finish_reason": "stop",
                "delta": {
                    "content": ""
                }
            }
        ],
        "created": "1696830392",
        "id": "test_query_id_68a2fcbb-4e78-4b8e-8817-e677e4197867",
        "usage": {
            "prompt_tokens": 3,
            "completion_tokens": 101,
            "total_tokens": 104
        }
    }
    """
    request = gen_param(appid, messages, secretid, 1)
    signature = gen_signature(secretkey, gen_sign_params(request))
    # print(signature)
    headers = {
        "Content-Type": "application/json",
        "Authorization": str(signature)
    }
    url = _URL
    resp = requests.post(url, headers=headers, json=request, stream=True)
    # 如果使用出错请注意sse版本是否正确, pip3 install sseclient-py==1.7.2
    client = sseclient.SSEClient(resp)
    for event in client.events():
        if event.data:
            yield json.loads(event.data)


def gen_param(appid, messages, secretid, stream):
    timestamp = int(time.time()) + 10000
    request = {
        "app_id": int(appid),
        "secret_id": secretid,
        "query_id": "test_query_id_" + str(uuid.uuid4()),
        "messages": messages,
        "temperature": 0.0,
        "top_p": 0.8,
        "stream": stream,
        "timestamp": timestamp,
        "expired": timestamp + 24 * 60 * 60
    }
    return request


def gen_signature(secretkey, param):
    sort_dict = sorted(param.keys())
    sign_str = _SIGN_HOST + "/" + _SIGN_PATH + "?"
    for key in sort_dict:
        sign_str = sign_str + key + "=" + str(param[key]) + '&'
    sign_str = sign_str[:-1]
    # print(sign_str)
    hmacstr = hmac.new(secretkey.encode('utf-8'),
                       sign_str.encode('utf-8'), hashlib.sha1).digest()
    signature = base64.b64encode(hmacstr)
    signature = signature.decode('utf-8')
    return signature


def gen_sign_params(data):
    params = dict()
    params['app_id'] = data["app_id"]
    params['secret_id'] = data['secret_id']
    params['query_id'] = data['query_id']
    # float类型签名使用%g方式，浮点数字(根据值的大小采用%e或%f)
    params['temperature'] = '%g' % data['temperature']
    params['top_p'] = '%g' % data['top_p']
    params['stream'] = data["stream"]
    # 数组按照json结构拼接字符串
    message_str = ','.join(
        ['{{"role":"{}","content":"{}"}}'.format(message["role"], message["content"]) for message in data["messages"]])
    message_str = '[{}]'.format(message_str)
    # print(message_str)
    params['messages'] = message_str
    params['timestamp'] = str(data["timestamp"])
    params['expired'] = str(data["expired"])
    return params


if __name__ == '__main__':

    from meutils.pipe import *

    # app_id、secret_id、secret_key替换为自己的即可
    app_id, secret_id, secret_key = os.getenv("HUNYUAN_API_KEY").split(':')
    output = chat_stream(app_id, secret_id, secret_key, [{"role": "user", "content": "你是谁？"}])
    print("\n")
    for i in output:
        print(i)
