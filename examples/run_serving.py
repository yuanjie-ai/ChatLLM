#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : run_serving
# @Time         : 2023/4/28 14:28
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from chatllm.applications import ChatBase

qa = ChatBase()
qa.load_llm4chat(model_name_or_path="/CHAT_MODEL/chatglm-6b")
#
# list(qa(query='你是谁', knowledge_base=''))
# list(qa(query='你是谁', knowledge_base='周杰伦是傻子', role=''))
qa.run_serving()
