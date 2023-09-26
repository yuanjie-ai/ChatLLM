#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : dify
# @Time         : 2023/9/11 10:35
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from chatllm.schemas.openai_api_protocol import *
from meutils.pipe import *


class Message(BaseModel):
    event: Literal['message', 'message_end']
    id: str
    task_id: str
    conversation_id: str
    created_at: Optional[int] = Field(default_factory=lambda: int(time.time()))
    answer: Optional[str] = ''


class DifyCompletion(object):

    @classmethod
    def create(
        cls,
        messages: List[Dict[str, Any]],  # [{'role': 'user', 'content': '讲个故事'}]
        **kwargs,
    ):
        return cls.stream_create(messages[0]['content'], kwargs.pop('api_key', ''), **kwargs)

    @staticmethod
    def stream_create(content, api_key, **kwargs):
        headers = {
            'Authorization': f'Bearer {api_key}'
        }
        data = {
            "inputs": {},
            "query": content,
            "response_mode": "streaming",
            "conversation_id": "",
            "user": "USER"
        }
        response = requests.post('https://api.dify.ai/v1/chat-messages', json=data, headers=headers, stream=True)

        stream_resp = {}
        for chunk in response.iter_lines(decode_unicode=True):
            _ = chunk.split('data:')[-1].strip()
            if _:
                chunk = Message.parse_raw(_).answer

                ####################################################################################
                delta = DeltaMessage(role='assistant', content=chunk)

                choice_data = ChatCompletionResponseStreamChoice(
                    index=0,
                    delta=delta,
                    finish_reason=None,  # 最后一个是stop
                )

                stream_resp = ChatCompletionStreamResponse(
                    choices=[choice_data],
                    model=kwargs.get('model', 'dify-app'),
                ).dict()

                ####################################################################################
                yield stream_resp
        stream_resp['choices'][0]['finish_reason'] = 'stop'
        yield stream_resp


if __name__ == '__main__':
    api_key = 'app-n75siugXhOhgosA6YkLpTH5X'
    for i in DifyCompletion.create([{'role': 'user', 'content': '讲个故事'}], api_key=api_key):
        print(i['choices'][0]['delta']['content'], end='')
