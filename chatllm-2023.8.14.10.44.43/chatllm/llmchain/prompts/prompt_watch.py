#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : promptwatch
# @Time         : 2023/7/13 10:03
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *

from langchain import OpenAI, LLMChain, PromptTemplate
from promptwatch import PromptWatch, register_prompt_template

prompt_template = PromptTemplate.from_template("这是个prompt： {input}")
prompt_template = register_prompt_template("name_of_your_template", prompt_template)
my_chain = LLMChain(llm=OpenAI(streaming=True), prompt=prompt_template)

with PromptWatch(api_key=os.getenv('PROMPT_WATCH_API_KEY')) as pw:
    my_chain("1+1=")
