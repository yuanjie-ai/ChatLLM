#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : __init__.py
# @Time         : 2023/6/30 21:49
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 异步缓存 from aiocache import cached
import os

from meutils.pipe import *

import openai

OPENAI_EMBEDDINGS_CACHE = os.getenv("OPENAI_EMBEDDINGS_CACHE", "~/.cache/openai_embeddings_cache")

openai.Embedding.create = disk_cache(openai.Embedding.create, location=OPENAI_EMBEDDINGS_CACHE)

from langchain.embeddings import OpenAIEmbeddings as _OpenAIEmbeddings, HuggingFaceEmbeddings
#
#
# class OpenAIEmbeddings(_OpenAIEmbeddings):
#
#     @disk_cache(location=OPENAI_EMBEDDINGS_CACHE)
#     def _embedding_func(self, text: str, *, engine: str) -> List[float]:
#         return super()._embedding_func(text, engine=engine)
#
#     @disk_cache(location=OPENAI_EMBEDDINGS_CACHE)
#     def _get_len_safe_embeddings(
#         self, texts: List[str], *, engine: str, chunk_size: Optional[int] = None
#     ) -> List[List[float]]:
#         logger.info(texts)
#         return super()._get_len_safe_embeddings(texts, engine=engine, chunk_size=chunk_size)
