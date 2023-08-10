#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : sota_embedding
# @Time         : 2023/4/21 11:56
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from sentence_transformers import SentenceTransformer
from meutils.docarray_ import Document, DocumentArray


# 增加 docarray v2
# 增加 ann后端
class SentenceEmbedding(object):
    def __init__(self, model_name_or_path="shibing624/text2vec-base-chinese", **st_kwargs):
        """
            disk_cache()(SentenceEmbedding().encode)
        :param model_name_or_path:
        :param device:
        """
        self.st = SentenceTransformer(model_name_or_path, **st_kwargs)

    def __call__(self, *args, **kwargs):
        return self.encode(*args, **kwargs)

    def encode(self, sentences, batch_size=32, show_progress_bar=False, normalize_embeddings=False,
               return_document=False):

        if isinstance(sentences, str):
            sentences = [sentences]

        embeddings = self.st.encode(
            sentences,
            batch_size=batch_size,
            show_progress_bar=show_progress_bar,
            normalize_embeddings=normalize_embeddings
        )
        if return_document:
            da = DocumentArray.empty(len(sentences))
            da.texts = sentences
            da.embeddings = embeddings
            return da
        return embeddings
