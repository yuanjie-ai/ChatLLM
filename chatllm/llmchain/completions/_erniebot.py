#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : erniebot
# @Time         : 2023/9/7 10:36
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.cache_utils import ttl_cache
from meutils.decorators.retry import retrying
from chatllm.schemas.openai_api_protocol import *

import erniebot

models = erniebot.Model.list()
# Set authentication params
erniebot.api_type = "qianfan"
erniebot.ak = "APCEKzr4rU8ywqPxzDQn0rCn1"
erniebot.sk = "5ryzXEhNkk5DT9PeX3jLhZ1w3rsEUktn"


# erniebot.ChatCompletion.create(


class ErnieBotCompletion(object):

    @classmethod
    def create(
        cls,
        messages: List[Dict[str, Any]],  # [{'role': 'user', 'content': '讲个故事'}]
        **kwargs,
    ):
        api_key, secret_key = kwargs.pop('api_key').split(':')

        post_kwargs = {
            'url': cls.create_url(api_key, secret_key, **kwargs),
            'json': {
                'messages': messages,

                'stream': kwargs.get('stream'),
                'temperature': np.clip(kwargs.get('temperature', 0), 0.01, 1),
            },
            # 'stream': kwargs.get('stream')
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
        stream_resp['choices'][0]['finish_reason'] = 'stop'
        yield stream_resp


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
