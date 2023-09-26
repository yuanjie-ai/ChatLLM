#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : index_utils
# @Time         : 2023/9/11 17:37
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://python.langchain.com/docs/modules/data_connection/indexing#using-with-loaders

from meutils.pipe import *
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import SQLRecordManager, index
from langchain.schema import Document
from langchain.vectorstores import ElasticsearchStore, Chroma

collection_name = "test_index"

embedding = OpenAIEmbeddings()
namespace = f"chromadb/{collection_name}"
record_manager = SQLRecordManager(
    namespace, db_url="sqlite:///record_manager_cache.sql"
)
record_manager.create_schema()

vectorstore = Chroma(collection_name=collection_name, embedding_function=embedding)


def _clear():  # 清空向量
    """Hacky helper method to clear content. See the `full` mode section to to understand why it works."""
    index([], record_manager, vectorstore, cleanup="full", source_id_key="source")

# index(docs, record_manager, vectorstore, cleanup="full", source_id_key="source")
# index(loader, record_manager, vectorstore, cleanup="full", source_id_key="source") # source_id_key同一个文档不同段落



