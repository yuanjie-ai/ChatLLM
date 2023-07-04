#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : 流式输出
# @Time         : 2023/7/3 19:26
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
from llama_index.indices.query.query_transform.base import ImageOutputQueryTransform

from meutils.pipe import *

import langchain
# from langchain.prompts import Prompt

from langchain.cache import InMemoryCache, MomentoCache

from llama_index.llm_predictor.chatgpt import ChatGPTLLMPredictor

from llama_index import Prompt, SimpleDirectoryReader, load_index_from_storage, MockLLMPredictor, GPTTreeIndex, \
    MockEmbedding, GPTVectorStoreIndex

llm_predictor = ChatGPTLLMPredictor()
llm_predictor.llm.streaming = True
# langchain.llm_cache = InMemoryCache() # 流式会不奏效：重写缓存

p = Prompt('周杰伦')
p.get_langchain_prompt()
r, _ = llm_predictor.stream(p)
for i in r:
    print(i, end='')
llm_predictor = ChatGPTLLMPredictor()
llm_predictor.llm.streaming = True

# sd = SimpleDirectoryReader(input_files=['孙子兵法.pdf'])
