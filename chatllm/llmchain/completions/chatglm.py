#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chatglm
# @Time         : 2023/9/26 15:22
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.decorators.retry import retrying

from chatllm.schemas.openai_api_protocol import *


class ChatGLMCompletion(object):
    @classmethod
    def create(
        cls,
        messages: List[Dict[str, Any]],  # [{'role': 'user', 'content': '讲个故事'}]
        **kwargs,
    ):
        try_import('zhipuai')
        import zhipuai
        from zhipuai.model_api import api

        zhipuai.api_key = kwargs.pop('api_key')
        api.post = retrying(api.post, predicate=lambda x: x is None)
        api.stream = retrying(api.stream, predicate=lambda x: x is None)

        if kwargs.get('stream'):
            return cls._stream_create(messages, **kwargs)
        else:
            return cls._create(messages, **kwargs)

    @staticmethod
    def _create(messages, **kwargs):
        try_import('zhipuai')
        import zhipuai
        data = zhipuai.model_api.invoke(prompt=messages, **kwargs).get('data', {})
        choices = data.get('choices', [])
        if choices:
            choice = ChatCompletionResponseChoice(index=0, message=ChatMessage(**choices[0]), finish_reason='stop')
            _ = ChatCompletionResponse(
                model=kwargs.get('model', 'chatglm_lite'),
                choices=[choice],
                usage=UsageInfo(**data.pop('usage', {}))
            ).dict()
            return _
        return {}

    @staticmethod
    def _stream_create(messages, **kwargs):

        try_import('zhipuai')
        import zhipuai

        resp = zhipuai.model_api.sse_invoke(prompt=messages, **kwargs).events()

        finish_reason = None
        usage = UsageInfo()
        for event in resp:
            if event.event == 'finish':
                finish_reason = 'stop'
                usage = json.loads(event.meta).get('usage', {})
                usage = UsageInfo(**usage)

            delta = DeltaMessage(role='assistant', content=event.data)
            choice = ChatCompletionResponseStreamChoice(
                index=0,
                delta=delta,
                finish_reason=finish_reason,
            )
            stream_resp = ChatCompletionStreamResponse(
                choices=[choice],
                model=kwargs.get('model', 'chatglm_lite'),
                usage=usage
            ).dict()

            yield stream_resp


if __name__ == '__main__':
    from meutils.pipe import *

    r = ChatGLMCompletion.create(
        messages=[{'role': 'user', 'content': '1+1'}],
        stream=False,
        api_key=os.getenv('CHATGLM_API_KEY'),
        model='chatglm_lite'
    )
    print(r)
    for i in r:
        print(i)
