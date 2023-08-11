#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : base
# @Time         : 2023/7/5 09:32
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *

from langchain.vectorstores.base import Document, CallbackManagerForRetrieverRun
from langchain.vectorstores.base import VectorStoreRetriever as _VectorStoreRetriever

class VectorStoreRetriever(_VectorStoreRetriever):

    def _get_relevant_documents(
        self, query: str, *, run_manager: Optional[CallbackManagerForRetrieverRun]
    ) -> List[Document]:
        if self.search_type == "similarity":
            docs = self.vectorstore.similarity_search(query, **self.search_kwargs)
        elif self.search_type == "similarity_score_threshold":
            docs_and_similarities = (
                self.vectorstore.similarity_search_with_relevance_scores(
                    query, **self.search_kwargs
                )
            )

            # docs = [doc for doc, _ in docs_and_similarities]
            docs = []
            for doc, score in docs_and_similarities:
                logger.info(docs_and_similarities)
                doc.metadata['similarity_score'] = score
                docs.append(doc)

        elif self.search_type == "mmr":
            docs = self.vectorstore.max_marginal_relevance_search(
                query, **self.search_kwargs
            )
        else:
            raise ValueError(f"search_type of {self.search_type} not allowed.")
        return docs
