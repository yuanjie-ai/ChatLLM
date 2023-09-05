#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : faiss
# @Time         : 2023/8/10 16:21
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 比较 https://zhuanlan.zhihu.com/p/595249861?utm_id=0

from meutils.pipe import *
from langchain.vectorstores import FAISS as _FAISS
from langchain.embeddings.base import Embeddings
from langchain.docstore.base import AddableMixin, Docstore
from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
from langchain.vectorstores.utils import DistanceStrategy, maximal_marginal_relevance


class FAISS(_FAISS):
    """
    from chatllm.llmchain.vectorstores import FAISS
    from chatllm.llmchain.embeddings import HuggingFaceEmbeddings

    model_name = '/Users/betterme/PycharmProjects/AI/m3e-small'
    encode_kwargs = {'normalize_embeddings': True}
    embeddings = HuggingFaceEmbeddings(model_name=model_name, encode_kwargs=encode_kwargs)

    faiss1 = FAISS.from_texts(['1', '2', '3'], embeddings)
    faiss2 = FAISS.from_texts(['11', '22', '33'], embeddings)
    faiss1.merge_from(faiss2)
    faiss1.similarity_search('1')

    faiss1.save_local('faiss_data')
    faiss1 = FAISS.load_local('faiss_data', embeddings)

    """

    def __init__(
        self,
        embedding_function: Callable,
        index: Any,
        docstore: Docstore,
        index_to_docstore_id: Dict[int, str],
        relevance_score_fn: Optional[Callable[[float], float]] = None,
        normalize_L2: bool = False,
        distance_strategy: DistanceStrategy = DistanceStrategy.MAX_INNER_PRODUCT,
        **kwargs
    ):
        super().__init__(embedding_function, index, docstore, index_to_docstore_id, relevance_score_fn, normalize_L2,
                         distance_strategy)

    @classmethod
    def from_texts(
        cls,
        texts: List[str],
        embedding: Embeddings,
        metadatas: Optional[List[dict]] = None,
        ids: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> _FAISS:

        # 默认内积
        kwargs['distance_strategy'] = kwargs.get('distance_strategy', DistanceStrategy.MAX_INNER_PRODUCT)

        return super().from_texts(texts, embedding, metadatas, ids, **kwargs)

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None,
        fetch_k: int = 20,
        threshold: float = 0.5,
        **kwargs: Any,
    ) -> List[Document]:
        """Return docs most similar to query.
        faiss.as_retriever(search_kwargs={'k':1})

        Args:
            query: Text to look up documents similar to.
            k: Number of Documents to return. Defaults to 4.
            filter: (Optional[Dict[str, str]]): Filter by metadata. Defaults to None.
            fetch_k: (Optional[int]) Number of Documents to fetch before filtering.
                      Defaults to 20.
            threshold:

        Returns:
            List of Documents most similar to the query.
        """

        docs_and_scores = self.similarity_search_with_score(
            query, k, filter=filter, fetch_k=fetch_k, **kwargs
        )

        docs = []
        for doc, score in docs_and_scores:
            if score > threshold:
                doc.metadata['score'] = round(score, 2)
                docs.append(doc)
        return docs


if __name__ == '__main__':
    from chatllm.llmchain.vectorstores import FAISS
    from chatllm.llmchain.embeddings import HuggingFaceEmbeddings

    model_name = '/Users/betterme/PycharmProjects/AI/m3e-small'
    encode_kwargs = {'normalize_embeddings': True, 'show_progress_bar': True, 'device': 'mps'}
    embeddings = HuggingFaceEmbeddings(model_name=model_name, encode_kwargs=encode_kwargs)

    faiss1 = FAISS.from_texts(['1', '2', '3'], embeddings)
    faiss2 = FAISS.from_texts(['11', '22', '33'], embeddings)
    faiss1.merge_from(faiss2)
    print(faiss1.similarity_search('1'))

    # faiss1.save_local('faiss_data')
    # faiss1 = FAISS.load_local('faiss_data', embeddings)
