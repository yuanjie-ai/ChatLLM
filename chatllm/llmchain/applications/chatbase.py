#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chatdoc
# @Time         : 2023/7/15 20:53
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *

from chatllm.llmchain.utils import docs2dataframe
from chatllm.llmchain.decorators import llm_stream
from chatllm.llmchain.vectorstores import Milvus
from chatllm.llmchain.embeddings import OpenAIEmbeddings, DashScopeEmbeddings
from chatllm.llmchain.document_loaders import FilesLoader
from chatllm.llmchain.prompts.prompt_templates import context_prompt_template

from langchain.text_splitter import *
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.base import Embeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema import BaseLanguageModel
from langchain.vectorstores import VectorStore


class ChatBase(object):

    def __init__(self,
                 # 初始化 openai_api_key
                 llm: Optional[BaseLanguageModel] = None,
                 embeddings: Optional[Embeddings] = None,
                 vectorstore: Optional[VectorStore] = None,

                 collection_name: str = 'TEST',  # todo: 参数设置，llm_kwargs/embeddings_kwargs/vectorstore_kwargs

                 get_api_key: Optional[Callable[[int], List[str]]] = None,
                 prompt_template=context_prompt_template,

                 **kwargs
                 ):
        """

        :param llm:
        :param embeddings:
        :param collection_name:
        :param get_api_key:
        :param prompt_template:
        """
        self.llm = llm or ChatOpenAI(model="gpt-3.5-turbo-16k-0613", temperature=0, streaming=True)
        self.embeddings = embeddings or OpenAIEmbeddings(chunk_size=5)

        self.prompt_template = prompt_template  # cb.chain.llm_chain.prompt.messages

        # 向量数据库
        self.collection_name = collection_name
        _vdb_kwargs = self.vdb_kwargs.copy()
        _vdb_kwargs['embedding_function'] = _vdb_kwargs.pop('embedding')  # 参数一致性
        # _vdb_kwargs['drop_old'] = True # 重新创建
        self.vectorstore: Optional[Milvus] = vectorstore or Milvus(**_vdb_kwargs)  # 耗时吗

        # self.vectorstore.collection_name = collection_name # todo: 参数设置

        if get_api_key:
            self.llm.openai_api_key = get_api_key(1)[0]
            self.embeddings.get_api_key = get_api_key
            self.embeddings.openai_api_key = get_api_key(1)[0]

        self.chain = load_qa_chain(
            self.llm,
            chain_type="stuff",
            prompt=ChatPromptTemplate.from_template(prompt_template)  # todo: 增加上下文信息
        )

    def pipeline(self):
        pass

    def llm_qa(self, query: str, k: int = 5, threshold: float = 0.5, **kwargs: Any):
        """todo: pipeline"""
        docs = self.vectorstore.similarity_search(query, k=k, threshold=threshold, **kwargs)
        docs = docs | xUnique_plus(lambda doc: doc.page_content.strip())  # 按内容去重，todo: 按语义相似度去重
        docs = docs[:k]
        if docs:
            return llm_stream(self.chain.run)({"input_documents": docs, "question": query})  # todo: 空文档报错吗？
        else:
            logger.warning("Retrieval is empty, Please check the vector database ！！！")

    @staticmethod
    def load_file(
        file_paths,
        max_workers=3,
        chunk_size=2000,
        chunk_overlap=200,
        separators: Optional[List[str]] = None
    ) -> List[Document]:
        """支持多文件"""
        loader = FilesLoader(file_paths, max_workers=max_workers)
        separators = separators or ['\n\n', '\r', '\n', '\r\n', '。', '!', '！', '\\?', '？', '……', '…']
        textsplitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            add_start_index=True,
            separators=separators
        )
        docs = loader.load_and_split(textsplitter)
        return docs

    # @diskcache(location=os.getenv('INSERT_VECTOR_CACHE', '~/.cache/insert_vector_cache'), ignore=['self'])
    def create_index(self, docs: List[Document], **kwargs):
        """初始化 drop_old=True"""
        self.vectorstore = Milvus.from_documents(docs, **{**self.vdb_kwargs, **kwargs})

    @property
    def vdb_kwargs(self):
        connection_args = {
            'uri': os.getenv('ZILLIZ_ENDPOINT'),
            'token': os.getenv('ZILLIZ_TOKEN')
        }
        address = os.getenv('MILVUS_ADDRESS')  # 该参数优先
        if address:
            connection_args.pop('uri')
            connection_args['address'] = address

        index_params = {
            "metric_type": "IP",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 1024}
        }

        embedding_function = self.embeddings

        vdb_kwargs = dict(
            embedding=embedding_function,
            connection_args=connection_args,
            index_params=index_params,
            search_params=None,
            collection_name=self.collection_name,
            drop_old=False,
        )

        return vdb_kwargs
