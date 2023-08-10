#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : closeai
# @Time         : 2023/5/24 14:38
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo: 整合所有api
"""
openai
chatglm
ziya
bard
文心
讯飞
"""

from meutils.pipe import *
import openai

openai.api_base = 'https://api.openai-proxy.com/v1'
openai.api_key = "sk-xx"  # supply your API key however you choose


def create(prompt="1+1", stream=True, max_tokens=2048, model="text-davinci-003"):
    completion = openai.Completion.create(model=model, prompt=prompt, stream=stream, max_tokens=max_tokens)
    if not stream:
        return completion.choices[0].text
    for c in completion:
        yield c.choices[0].text
