#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ernie
# @Time         : 2023/7/31 16:34
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://cloud.baidu.com/doc/WENXINWORKSHOP/s/flfmc9do2

from meutils.pipe import *
from meutils.cache_utils import ttl_cache
from meutils.decorators.retry import retrying
from chatllm.datamodels.openai_api_protocol import *


class ErnieBotCompletion(object):

    @classmethod
    def create(
        cls,
        messages: List[Dict[str, Any]],  # [{'role': 'user', 'content': '讲个故事'}]
        **kwargs,
    ):
        print(kwargs)
        api_key, secret_key = kwargs.pop('api_key').split(':')
        post_kwargs = {
            'url': cls.create_url(api_key, secret_key, **kwargs),
            'json': {
                'messages': messages,

                'stream': kwargs.get('stream'),
                'temperature': np.clip(kwargs.get('temperature', 0), 0.01, 1),
            },
            'stream': kwargs.get('stream')
        }

        response = requests.post(**post_kwargs)
        # {'error_code': 17, 'error_msg': 'Open api daily request limit reached'}

        if kwargs.get('stream'):
            return cls.stream_create(response, **kwargs)

        else:
            resp = response.json()

            content = resp.pop('result')
            ####################################################################################
            message = ChatMessage(role='assistant', content=content)
            choice = ChatCompletionResponseChoice(
                index=0,
                message=message,
                finish_reason='stop'
            )
            _ = ChatCompletionResponse(
                model=kwargs.get('model', ''),
                choices=[choice],
                usage=UsageInfo(**resp.pop('usage', {}))
            ).dict()
            ####################################################################################
            return _

    @staticmethod
    def stream_create(response, **kwargs):
        _chunk = ''
        stream_resp = {}
        for chunk in response.iter_content(chunk_size=256, decode_unicode=True):
            _chunk += chunk
            if '\n\n' not in _chunk:  #
                continue

            chunks = _chunk.rsplit('\n\n', 1)
            _stream_resp = json.loads(chunks[0].strip('data: \n\n'))  # bug
            _chunk = chunks[1]

            content = _stream_resp.pop('result')

            ####################################################################################
            delta = DeltaMessage(role='assistant', content=content)

            choice_data = ChatCompletionResponseStreamChoice(
                index=0,
                delta=delta,
                finish_reason=None,  # 最后一个是stop
            )

            stream_resp = ChatCompletionStreamResponse(
                choices=[choice_data],
                model=kwargs.get('model', 'ernie-bot'),
            ).dict()

            stream_resp['usage'] = _stream_resp.pop('usage', {})
            ####################################################################################

            yield stream_resp

        # stream_resp['choices'][0]['finish_reason'] = 'stop'
        # yield stream_resp

        # stream_resp = stream_resp or json.loads(_chunk.strip('data: \n\n'))  # 只有一行

        # stream_resp['token_usage'] = stream_resp.pop('usage', {})
        # stream_resp['choices'] = [{"delta": {}, "index": 0, "finish_reason": "stop"}]
        # yield stream_resp

    @staticmethod
    @retrying
    @ttl_cache(ttl=7 * 24 * 3600)
    def create_url(api_key, secret_key, **kwargs):
        """
        使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
        """
        url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}"
        response = requests.request("POST", url)
        access_token = response.json().get("access_token")

        if 'ernie-bot-turbo' in kwargs.get('model', 'ernie-bot-turbo-0725'):
            route = 'eb-instant'
        else:
            route = 'completions'

        url = f'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{route}?access_token={access_token}'
        return url


if __name__ == '__main__':
    from meutils.pipe import *

    ec = ErnieBotCompletion()
    r = ec.create(
        [{'role': 'user', 'content': '杭州西力智能科技股份有限公司2021年营业利润增长率是多少?保留2位小数。'}],
        stream=True,
        api_key=os.getenv('ERNIE_API_KEY'),
        model='ernie-bot'
    )
    print(r)
    for i in r:
        print(i)
