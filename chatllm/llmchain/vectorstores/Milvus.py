#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : Milvus
# @Time         : 2023/7/14 17:40
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
from meutils.pipe import *
from langchain.docstore.document import Document
from langchain.vectorstores import Milvus as _Milvus


class Milvus(_Milvus):

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        param: Optional[dict] = None,
        expr: Optional[str] = None,
        timeout: Optional[int] = None,
        threshold: float = 0.5,
        **kwargs: Any,
    ) -> List[Document]:

        if self.col is None:
            logger.debug("No existing collection to search.")
            return []
        docs_scores = self.similarity_search_with_score(
            query=query, k=k, param=param, expr=expr, timeout=timeout, **kwargs
        )

        docs = []
        for doc, score in docs_scores:
            if score > threshold:
                doc.metadata['score'] = round(score, 2)
                docs.append(doc)
        return docs

    def similarity_search_by_batch(self):  # TODO todo
        """
                # todo: batch
        query 前处理
        recall 后处理/精排
        :return:
        """
        pass
