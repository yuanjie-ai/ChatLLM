#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2023/5/29 13:16
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *


def article_generator(keywords, api_key, max_tokens=2048):
    import openai
    openai.api_base = 'https://api.openai-proxy.com/v1'
    openai.api_key = api_key
    prompt = """
        你现在是位资深SEO优化专家，请通过尖括号里的关键词<{keywords}>，写一篇seo文章，
        要求返回标题与内容
        """.strip()
    model = "text-davinci-003"
    completion = openai.Completion.create(model=model, prompt=prompt, stream=True, max_tokens=max_tokens)
    for c in tqdm(completion, desc=keywords):
        yield c.choices[0].text
