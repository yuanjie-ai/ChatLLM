#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : llmcache
# @Time         : 2023/7/6 11:51
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://zhuanlan.zhihu.com/p/629348339

from meutils.pipe import *

from gptcache import cache
from gptcache.embedding import Onnx, OpenAI
from gptcache.manager import CacheBase, VectorBase, get_data_manager
from gptcache.similarity_evaluation import SearchDistanceEvaluation, ExactMatchEvaluation
from gptcache.processor.pre import get_prompt
from gptcache.adapter.api import init_similar_cache


def get_msg_func(data, **_):
    return data.get("messages")[-1].content


onnx = Onnx()
cache_base = CacheBase('sqlite')
vector_base = VectorBase('faiss', dimension=onnx.dimension)
data_manager = get_data_manager(cache_base, vector_base)
cache.init(
    pre_embedding_func=get_msg_func,
    embedding_func=onnx.to_embeddings,
    data_manager=data_manager,
    similarity_evaluation=SearchDistanceEvaluation(),
)
cache.set_openai_key()


from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
