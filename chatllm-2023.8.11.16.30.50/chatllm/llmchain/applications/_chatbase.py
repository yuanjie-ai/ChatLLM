#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chatbase
# @Time         : 2023/7/5 15:29
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from langchain.schema import Document

from langchain.chat_models import ChatOpenAI
from langchain.cache import InMemoryCache
from langchain.memory import ConversationBufferWindowMemory
from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings.base import Embeddings
from langchain.vectorstores import VectorStore, DocArrayInMemorySearch, Zilliz, FAISS
from langchain.callbacks import AsyncIteratorCallbackHandler

from langchain.chains.question_answering import load_qa_chain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain  # 输出SOURCE废token
from langchain.chains import ConversationChain
from langchain.document_loaders import DirectoryLoader, PyMuPDFLoader


# import langchain
#
# langchain.verbose = True
# langchain.debug = True


class ChatBase(object):
    """
    ChatBase().create_index().search().run(query='1+1')
    """

    def __init__(self, model="gpt-3.5-turbo", embeddings: Embeddings = OpenAIEmbeddings(chunk_size=100), k=1,
                 temperature=0):
        self.memory = ConversationBufferWindowMemory(memory_key="chat_history", return_messages=True, k=k)
        self.memory_messages = self.memory.chat_memory.messages
        self.embeddings = embeddings  # todo: 本地向量
        self.llm = ChatOpenAI(model=model, temperature=temperature, streaming=True)
        self.chain = load_qa_chain(self.llm, chain_type="stuff")  # map_rerank 重排序
        #
        self._docs = None
        self._index = None
        self._input = None

    def create_index(self, docs: List[Document], vectorstore: VectorStore = DocArrayInMemorySearch):  # 主要耗时，缓存是否生效
        self._index = vectorstore.from_documents(docs, self.embeddings)  # 向量阶段：可以多线程走缓存？
        return self

    def search(self, query, k: int = 5, threshold: float = 0.7, **kwargs):
        docs_scores = self._index.similarity_search_with_score(query, k=k, **kwargs)
        self._docs = []
        for doc, score in docs_scores:
            if score > threshold:
                doc.metadata['score'] = score
                doc.metadata['page_content'] = doc.page_content
                self._docs.append(doc)

        self._input = {"input_documents": self._docs, "question": query}  # todo: input_func

        return self

    def run(self):
        return self.chain.run(self._input)  # 流式

