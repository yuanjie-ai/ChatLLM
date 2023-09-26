#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : spark
# @Time         : 2023/8/1 12:20
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

"""
https://github.com/allwefantasy/byzer-llm/blob/df581d8fb69fb3fa3d48782e5bf47797310c37a8/src/byzerllm/saas/sparkdesk/__init__.py#L69  ########
https://github.com/vital121/LLM-Kit/blob/f81a678dbee6db4ed195da17e278083c45c478f4/modules/model/use_api.py#L151
https://github.com/lichuanqi/Python_Learn_Note/blob/c6dc1c47ef9033035802219538bf5ee3c07eef6e/packages/langchain_/llm_.py#L220
"""
import ssl
import hmac
import hashlib
import websocket
import _thread as thread

from urllib.parse import urlparse, urlencode

# ME
from meutils.pipe import *
from chatllm.schemas.openai_api_protocol import *


class SparkBotCompletion(object):

    @classmethod
    def create(
        cls,
        messages: List[Dict[str, Any]],  # [{'role': 'user', 'content': '讲个故事'}]
        **kwargs,
        # {'model': 'gpt-3.5-turbo', 'request_timeout': None, 'max_tokens': None, 'stream': False, 'n': 1, 'temperature': 0.7, 'api_key': 'sk-...', 'api_base': 'https://api.openai-proxy.com/v1', 'organization': ''}
    ):
        appid, api_key, secret_key = kwargs.pop('api_key').split(':')
        url = cls.create_url(api_key, secret_key)

        # WS
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(
            url,
            on_message=cls.on_message,
            on_open=cls.on_open,
            on_close=cls.on_close,
            on_error=cls.on_error,
        )
        # 参数设置
        ws.messages = messages
        ws.response_queue = Queue()
        kwargs['appid'] = appid
        for k, v in kwargs.items():  # ws.temperature = temperature
            setattr(ws, k, v)

        if kwargs.get('stream'):
            background_tasks.add_task(ws.run_forever, sslopt={"cert_reqs": ssl.CERT_NONE})
            return cls.stream_create(ws.response_queue)

        else:
            ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
            resp = None
            response = {}
            for i, response in enumerate(cls.stream_create(ws.response_queue)):
                if i == 0:
                    resp = response
                    resp['choices'][0]['finish_reason'] = 'stop'
                    resp['choices'][0]['message'] = resp['choices'][0].pop('delta')

                else:
                    resp['choices'][0]['message']['content'] += response['choices'][0]['delta']['content']
            resp['usage'] = response.pop('usage', {})
            return resp

    @staticmethod
    def stream_create(response_queue):  # 取数
        while 1:
            _ = response_queue.get()
            if _ is None: break
            yield _

    @staticmethod
    def on_message(ws, message):
        data = json.loads(message)
        code = data['header']['code']
        if code != 0:
            ws.close()
            raise f'请求错误: {code}, {data}'
        else:
            payload = data["payload"]
            choices = payload["choices"]

            ####################################################################################
            delta = DeltaMessage(**choices["text"][0])

            choice_data = ChatCompletionResponseStreamChoice(
                index=0,
                delta=delta,
                finish_reason=None,
            )

            chunk = ChatCompletionStreamResponse(
                choices=[choice_data],
                model=ws.model,
            ).dict()

            chunk['usage'] = payload.pop('usage', {}).pop('text', {})
            ####################################################################################

            if choices["status"] == 2:
                chunk['choices'][0]['finish_reason'] = 'stop'
                ws.response_queue.put(chunk)  # 存数
                ws.response_queue.put(None)
                ws.close()
            else:
                ws.response_queue.put(chunk)

    @staticmethod
    def on_open(ws):
        thread.start_new_thread(SparkBotCompletion.run, (ws,))

    @staticmethod
    def on_error(ws, error):
        pass

    @staticmethod
    def on_close(ws, a, b):
        pass

    @staticmethod
    def run(ws, *args):
        # 8192
        data = {
            "header": {
                "app_id": ws.appid,
                "uid": "ws.uid",
            },
            "parameter": {
                "chat": {
                    "domain": "generalv2",  # [general,generalv2]
                    "random_threshold": ws.temperature,
                    "max_tokens": ws.max_tokens or 4096,  # 取值为[1,4096]，默认为2048，模型回答的tokens的最大长度
                    "auditing": "default"
                }
            },
            "payload": {
                "message": {
                    "text": ws.messages  # [{'role': 'user', 'content': '讲个故事'}]，所有content的累计tokens需控制8192以内
                }
            }
        }
        data = json.dumps(data)
        ws.send(data)

    @staticmethod
    def create_url(api_key, api_secret):
        from time import mktime
        from datetime import datetime
        from wsgiref.handlers import format_date_time

        # gpt_url = "ws://spark-api.xf-yun.com/v1.1/chat"
        gpt_url = "ws://spark-api.xf-yun.com/v2.1/chat"

        host = urlparse(gpt_url).netloc
        path = urlparse(gpt_url).path

        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": host
        }
        # 拼接鉴权参数，生成url
        url = f"{gpt_url}?{urlencode(v)}"
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url


if __name__ == '__main__':
    from meutils.pipe import *

    api_key = os.getenv('SPARK_API_KEY')
    # appid, api_key, secret_key = api_key.split(':')
    # print(SparkBotCompletion.create_url(api_key, secret_key))

    kw = {'model': 'gpt-3.5-turbo', 'request_timeout': None, 'max_tokens': None, 'stream': True, 'n': 1,
          'temperature': 0.7, 'api_key': api_key, 'api_base': 'https://api.openai-proxy.com/v1', 'organization': ''}
    g = SparkBotCompletion.create([{'role': 'user', 'content': '1+1'}], **kw)
    rprint(g)
    for i in g:
        print(i)
