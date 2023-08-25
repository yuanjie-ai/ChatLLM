#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : vdb
# @Time         : 2023/8/7 13:42
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from langchain.docstore.document import Document
from langchain.vectorstores import DocArrayInMemorySearch as _DocArrayInMemorySearch


class DocArrayInMemorySearch(_DocArrayInMemorySearch):

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        threshold: float = 0.5,
        **kwargs: Any,
    ) -> List[Document]:

        docs_scores = self.similarity_search_with_score(query=query, k=k, **kwargs)

        docs = []
        for doc, score in docs_scores:
            if score > threshold:
                doc.metadata['score'] = round(score, 2)
                docs.append(doc)
        return docs
