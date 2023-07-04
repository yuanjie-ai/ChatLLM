#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : client
# @Time         : 2023/5/30 16:39
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
import openai


def completion(
    prompt='你好', history=None, chat=False,
    api_base='https://api.openai-proxy.com/v1',  # https://t.me/openai_proxy
    api_key='sk-'
):
    openai.api_base = api_base
    openai.api_key = api_key
    kwargs = {
        "model": "gpt-3.5-turbo",
        "stream": True,
        "max_tokens": 1000,
        "temperature": None,
        "top_p": None,

        "user": "Betterme"
    }
    if is_open('0.0.0.0:8000'):
        logger.debug("本地大模型")
        openai.api_base = 'http://0.0.0.0:8000/v1'
        openai.api_key = 'chatllm'

    if chat:
        history = history or []  # [{"role": "system", "content": "你是东北证券大模型"}]
        kwargs['messages'] = history + [{"role": "user", "content": prompt}]
        completion = openai.ChatCompletion.create(**kwargs)
        response = ''
        for c in completion:
            _ = c.choices[0].get('delta').get('content', '')
            response += _
            print(_, flush=True, end='')
        # print('\n', response)

    else:
        kwargs['prompt'] = prompt
        kwargs['model'] = "text-davinci-003"
        completion = openai.Completion.create(**kwargs)
        response = ''
        for c in completion:
            _ = c.choices[0].text
            response += _
            print(_, flush=True, end='')
    return response


if __name__ == '__main__':
    # completion(prompt='你是谁', chat=True)
    completion(prompt='你是谁', chat=True)
