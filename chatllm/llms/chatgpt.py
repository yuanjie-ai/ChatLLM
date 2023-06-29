#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chatgpt
# @Time         : 2023/6/29 08:52
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *


def load_llm4chat(**kwargs):
    import openai

    openai.api_key = os.getenv("API_KEY", kwargs.get('api_key', 'chatllm'))
    openai.api_base = os.getenv("API_BASE", kwargs.get('api_base', "https://api.openai-proxy.com/v1"))

    def stream_chat(query, history=None):
        history = history or []  # [{"role": "system", "content": "你是东北证券大模型"}]
        messages = history + [{"role": "user", "content": query}]

        chat_kwargs = {
            "model": "gpt-3.5-turbo-16k-0613",
            "stream": True,
            "max_tokens": 16000,
            "temperature": None,
            "top_p": None,
            "messages": messages,
            "user": "Betterme"
        }
        completion = openai.ChatCompletion.create(**chat_kwargs)

        for c in completion:
            _ = c.choices[0].get('delta').get('content', '')
            yield _

    return stream_chat


if __name__ == '__main__':
    pass
