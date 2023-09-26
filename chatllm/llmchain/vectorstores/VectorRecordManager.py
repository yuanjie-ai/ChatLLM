#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : VectorRecordManager
# @Time         : 2023/9/12 13:40
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://python.langchain.com/docs/modules/data_connection/indexing#using-with-loaders

from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import SQLRecordManager, index
from langchain.schema import Document
from langchain.vectorstores import Chroma, VectorStore
from langchain.document_loaders.base import BaseLoader

from meutils.pipe import *
from chatllm.llmchain.vectorstores import ElasticsearchStore


class VectorRecordManager(object):
    """
    增量更新向量
        manager.vectorstore.similarity_search(
        'doc',
        filter=[{'term': {'metadata.source': 'unknown'}}]
    )
    """

    def __init__(
        self, collection_name="test_index",
        vectorstore: Optional[VectorStore] = None,
        db_url: Optional[str] = None,
    ):
        """

        :param collection_name:
        :param vectorstore:
            # 本地
            vectorstore = Chroma(collection_name=collection_name, embedding_function=embedding)

        :param db_url:
            # 默认在 HOME_CACHE
            f"sqlite:///{HOME_CACHE}/chatllm/vector_record_manager.sql"

            "sqlite:///chatllm_vector_record_manager_cache.sql"

        """
        self.collection_name = collection_name
        self.vectorstore = vectorstore or ElasticsearchStore(
            embedding=OpenAIEmbeddings(),
            index_name=self.collection_name,  # 同一模型的embedding
            es_url=os.getenv('ES_URL'),
            es_user=os.getenv('ES_USER'),
            es_password=os.getenv('ES_PASSWORD'),
        )
        namespace = f"{self.vectorstore.__class__.__name__}/{collection_name}"
        db_url = db_url or f"sqlite:///{HOME_CACHE / 'chatllm/vector_record_manager.sql'}"

        self.record_manager = SQLRecordManager(namespace, db_url=db_url)
        self.record_manager.create_schema()

    def update(
        self,
        docs_source: Union[List[str], BaseLoader, Iterable[Document]],
        cleanup: Literal["incremental", "full", None] = "incremental",
        source_id_key: Union[str, Callable[[Document], str], None] = "source",
    ):
        """

        :param docs_source:
        :param cleanup:
        :param source_id_key: 根据 metadata 信息去重
        :return:
        """
        if isinstance(docs_source, List) and isinstance(docs_source[0], str):
            docs_source = [Document(page_content=text, metadata={"source": 'unknown'}) for text in docs_source]

        return index(docs_source, self.record_manager, self.vectorstore, cleanup=cleanup, source_id_key=source_id_key)

    def _clear(self):
        return index([], self.record_manager, self.vectorstore, cleanup="full", source_id_key="source")


if __name__ == '__main__':
    doc1 = Document(page_content="kitty", metadata={"source": "kitty.txt"})
    doc2 = Document(page_content="doggy", metadata={"source": "doggy.txt"})

    manager = VectorRecordManager()
    print(manager._clear())
    # print(manager.update([doc1] * 3))
