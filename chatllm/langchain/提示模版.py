#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : 提示模版
# @Time         : 2023/7/4 08:47
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *

from langchain import LLMChain, OpenAI, PromptTemplate

prompt_template = "Tell me a {adjective} joke"
prompt = PromptTemplate.from_template(prompt_template)  # 自动化



from llama_index import Prompt

Prompt(prompt_template)
Prompt(prompt_template).get_langchain_prompt()
