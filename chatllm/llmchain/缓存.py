#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : 缓存
# @Time         : 2023/7/4 10:59
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://python.langchain.com/docs/modules/model_io/models/llms/integrations/llm_caching#gptcache
from langchain.schema import HumanMessage

from meutils.pipe import *
import time


def response_text(openai_resp):
    return openai_resp['choices'][0]['message']['content']


print("Cache loading.....")

# To use GPTCache, that's all you need
# -------------------------------------------------
from gptcache import cache
from gptcache.adapter import openai

cache.init()
# -------------------------------------------------

question = "周杰伦是谁，50字总结"
for _ in range(2):
    start_time = time.time()
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                'role': 'user',
                'content': question
            }
        ],
    )
    print(f'Question: {question}')
    print("Time consuming: {:.2f}s".format(time.time() - start_time))
    print(f'Answer: {response_text(response)}\n')



from gptcache import cache
from gptcache.processor.pre import get_prompt
# init gptcache
cache.init(pre_embedding_func=get_prompt)

from langchain.llms import OpenAI
from gptcache.adapter.langchain_models import LangChainLLMs
# run llm with gptcache
llm = LangChainLLMs(llm=OpenAI(temperature=0))
llm("Hello world")


from gptcache import cache
from gptcache.processor.pre import get_messages_last_content
# init gptcache
cache.init(pre_embedding_func=get_messages_last_content)
cache.set_openai_key()
from langchain.chat_models import ChatOpenAI
from gptcache.adapter.langchain_models import LangChainChat
# run chat model with gptcache
chat = LangChainChat(chat=ChatOpenAI(temperature=0))
chat([HumanMessage(content="Translate this sentence from English to French. I love programming.")])
