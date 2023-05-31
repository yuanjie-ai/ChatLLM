#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : config
# @Time         : 2023/5/26 13:08
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.decorators import clear_cuda_cache

from chatllm.llms import load_llm4chat

torch_gc = clear_cuda_cache(lambda: logger.info('Clear GPU'), bins=os.getenv('TIME_INTERVAL', 15))

######################配置#####################################
tokens = set(os.getenv('TOKENS', 'chatllm').split(','))
llm_model = os.getenv('LLM_MODEL', '')
embedding_model = os.getenv('EMBEDDING_MODEL')
device = os.getenv('DEVICE', 'cpu')
num_gpus = os.getenv('NUM_GPUS', 2)

llm_role = os.getenv('LLM_ROLE', '')
###############################################################


if embedding_model:
    from sentence_transformers import SentenceTransformer

    embedding_model = SentenceTransformer(embedding_model)
else:
    class RandomSentenceTransformer:
        def encode(self, texts):
            logger.error("请配置 EMBEDDING_MODEL")
            return np.random.random((len(texts), 64))


    embedding_model = RandomSentenceTransformer()

# 获取 do_chat
_do_chat = load_llm4chat(model_name_or_path=llm_model, device=device, num_gpus=num_gpus)


def do_chat(query, **kwargs):
    if llm_role:
        query = """{role}\n请回答以下问题\n{question}""".format(question=query, role=llm_role)  # 增加角色扮演
    return _do_chat(query, **kwargs)
