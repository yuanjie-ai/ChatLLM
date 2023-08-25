#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : __init__.py
# @Time         : 2023/6/30 16:37
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

import openai
from meutils.pipe import *
from meutils.cache_utils import diskcache, joblib_cache


@lru_cache
def init_cache(verbose=-1):
    CACHE = os.getenv("CHATLLM_CACHE", "~/.cache/chatllm")

    openai.Embedding.create = diskcache(
        openai.Embedding.create,
        location=f"{CACHE}/openai.Embedding.create",
        verbose=verbose,
    )

    try:

        from sentence_transformers import SentenceTransformer
        SentenceTransformer.encode = diskcache(
            SentenceTransformer.encode,
            location=f"{CACHE}/SentenceTransformer.encode",
            ignore=['self'],
            verbose=verbose,
        )
    except Exception as e:
        logger.warning(e)

    # SentenceTransformer.encode = joblib_cache(
    #     SentenceTransformer.encode,
    #     location=f"{CACHE}__SentenceTransformer",
    #     verbose=verbose,
    # )

    # try:
    #     import dashscope # 返回对象不支持序列化
    #     dashscope.TextEmbedding.call = set_cache(dashscope.TextEmbedding.call, verbose=verbose)
    # except Exception as e:
    #     logger.error(e)

    # 流式会生成不了
    # openai.Completion.create = diskcache(
    #     openai.Completion.create,
    #     location=f"{OPENAI_CACHE}_Completion",
    #     verbose=verbose,
    #     ttl=24 * 3600
    # )
    #
    # openai.ChatCompletion.create = diskcache(
    #     openai.ChatCompletion.create,
    #     location=f"{OPENAI_CACHE}_ChatCompletion",
    #     verbose=verbose,
    #     ttl=24 * 3600
    # )


if __name__ == '__main__':
    from langchain.embeddings import OpenAIEmbeddings

    print(OpenAIEmbeddings().embed_query(text='chatllmxxx'))
