#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : HuggingFaceBgeEmbeddings
# @Time         : 2023/8/10 15:32
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from langchain.embeddings import HuggingFaceEmbeddings as _HuggingFaceEmbeddings
from langchain.embeddings import HuggingFaceBgeEmbeddings as _HuggingFaceBgeEmbeddings


class HuggingFaceEmbeddings(_HuggingFaceEmbeddings):
    pre_fn: Optional[Callable[[str], str]] = None

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if self.pre_fn: texts = texts | xmap_(self.pre_fn)
        return super().embed_documents(texts)


class HuggingFaceBgeEmbeddings(_HuggingFaceBgeEmbeddings):
    pre_fn: Optional[Callable[[str], str]] = None

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if self.pre_fn: texts = texts | xmap_(self.pre_fn)
        return super().embed_documents(texts)


if __name__ == '__main__':
    model_name = '/Users/betterme/PycharmProjects/AI/m3e-small'
    pre_fn = lambda x: '句子太长' if len(x) > 500 else x

    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    embeddings.pre_fn = pre_fn

    print(embeddings.embed_documents(['']))
