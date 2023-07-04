#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : OpenAIChat
# @Time         : 2023/6/30 17:04
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from langchain.llms import OpenAIChat

os.environ['OPENAI_API_BASE'] = "https://api.openai-proxy.com/v1"

OpenAIChat()


class LLMChat(OpenAIChat):
    """兼容任意大模型"""
    pass
