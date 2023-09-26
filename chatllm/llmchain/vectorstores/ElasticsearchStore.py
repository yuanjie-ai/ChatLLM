#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ElasticsearchStore
# @Time         : 2023/9/18 15:40
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from langchain.docstore.document import Document
from langchain.vectorstores import ElasticsearchStore as _ElasticsearchStore, VectorStore

from meutils.pipe import *
from meutils.decorators.retry import retrying


class ElasticsearchStore(_ElasticsearchStore):

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter: Optional[List[dict]] = None,
        threshold: float = 0.5,
        **kwargs: Any,
    ) -> List[Document]:

        docs_and_scores = self._search(query=query, k=k, filter=filter, **kwargs)
        docs = []
        for doc, score in docs_and_scores:
            if score > threshold:
                doc.metadata['score'] = round(score, 2)
                docs.append(doc)
        return docs

    @retrying
    def _search(
        self,
        query: Optional[str] = None,
        k: int = 4,
        query_vector: Union[List[float], None] = None,
        fetch_k: int = 50,
        fields: Optional[List[str]] = None,
        filter: Optional[List[dict]] = None,
        custom_query: Optional[Callable[[Dict, Union[str, None]], Dict]] = None,
    ) -> List[Tuple[Document, float]]:
        return super()._search(query, k, query_vector, fetch_k, fields, filter, custom_query)

    @staticmethod
    def connect_to_elasticsearch(
        *,
        es_url: Optional[str] = None,
        cloud_id: Optional[str] = None,
        api_key: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        try:
            import elasticsearch
        except ImportError:
            raise ImportError(
                "Could not import elasticsearch python package. "
                "Please install it with `pip install elasticsearch`."
            )

        if es_url and cloud_id:
            raise ValueError(
                "Both es_url and cloud_id are defined. Please provide only one."
            )

        connection_params: Dict[str, Any] = {}

        if es_url:
            connection_params["hosts"] = [es_url]
        elif cloud_id:
            connection_params["cloud_id"] = cloud_id
        else:
            raise ValueError("Please provide either elasticsearch_url or cloud_id.")

        if api_key:
            connection_params["api_key"] = api_key
        elif username and password:
            connection_params["basic_auth"] = (username, password)

        #########################新增#########################
        # 第一次失败，第二次成功，需要加重试逻辑
        # 在做任何操作之前，先进行嗅探
        sniff_on_start = True

        # 节点没有响应时，进行刷新，重新连接
        sniff_on_node_failure = True

        # 每 60 秒刷新一次
        min_delay_between_sniffing = 60
        ######################################################

        es_client = elasticsearch.Elasticsearch(
            **connection_params,
            sniff_on_start=sniff_on_start,
            sniff_on_node_failure=sniff_on_node_failure,
            min_delay_between_sniffing=min_delay_between_sniffing
        )
        try:
            es_client.info()
        except Exception as e:
            logger.error(f"Error connecting to Elasticsearch: {e}")
            raise e

        return es_client
