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
from chatllm.llmchain.vectorstores import Milvus, FAISS
from chatllm.llmchain.embeddings import OpenAIEmbeddings, DashScopeEmbeddings
from chatllm.llmchain.document_loaders import FilesLoader
from chatllm.llmchain.prompts.prompt_templates import context_prompt_template

from langchain.text_splitter import *
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.base import Embeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.language_model import BaseLanguageModel
from langchain.vectorstores.base import VectorStore


class ChatFile(object):

    def __init__(
        self,
        # 初始化 openai_api_key
        llm: Optional[BaseLanguageModel] = None,
        embeddings: Optional[Embeddings] = None,
        vectorstore_cls=None,

        get_api_key: Optional[Callable[[int], List[str]]] = None,
        prompt_template=context_prompt_template,

        **kwargs
    ):
        self.llm = llm or ChatOpenAI(model="gpt-3.5-turbo-16k-0613", temperature=0, streaming=True)
        self.llm.streaming = True
        self.embeddings = embeddings or OpenAIEmbeddings(chunk_size=5)
        self.vectorstore = None
        self.vectorstore_cls: VectorStore = vectorstore_cls or FAISS

        self.prompt_template = prompt_template

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

    def create_index(self, docs: List[Document], **kwargs):
        """初始化 drop_old=True"""
        self.vectorstore = self.vectorstore_cls.from_documents(docs, **{**self.vdb_kwargs, **kwargs})

    def llm_qa(self, query: str, k: int = 5, threshold: float = 0.5, **kwargs: Any):
        assert self.vectorstore is not None, "Please create index."

        docs = self.vectorstore.similarity_search(query, k=k, threshold=threshold, **kwargs)
        docs = docs | xUnique_plus(lambda doc: doc.page_content.strip())  # 按内容去重，todo: 按语义相似度去重
        docs = sorted(docs, key=lambda doc: doc.metadata.get('index', 0))

        docs = docs[:k]
        if docs:
            return llm_stream(self.chain.run)({"input_documents": docs, "question": query})  # todo: 空文档报错吗？
        else:
            logger.warning("Retrieval is empty, Please check the vector database ！！！")
            # yield from "无相关文档"

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

    @property
    def vdb_kwargs(self):
        """
            # 向量数据库
            self.collection_name = collection_name
            # _vdb_kwargs = self.vdb_kwargs.copy()
            # _vdb_kwargs['embedding_function'] = _vdb_kwargs.pop('embedding')  # 参数一致性
            # # _vdb_kwargs['drop_old'] = True # 重新创建
            # self.vectorstore = vectorstore or Milvus(**_vdb_kwargs)  # 耗时吗
        :return:
        """
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
            collection_name=None,
            drop_old=False,
        )

        return vdb_kwargs


if __name__ == '__main__':
    from chatllm.llmchain.applications import ChatBase
    from chatllm.llmchain.embeddings import HuggingFaceEmbeddings
    from chatllm.llmchain.vectorstores import FAISS, Milvus

    model_name = '/Users/betterme/PycharmProjects/AI/m3e-small'
    encode_kwargs = {'normalize_embeddings': True, "show_progress_bar": True}
    embeddings = HuggingFaceEmbeddings(model_name=model_name, encode_kwargs=encode_kwargs)

    docs = [Document(page_content='1')] * 10
    faiss = FAISS.from_documents(docs, embeddings)

    cb = ChatBase(vectorstore=FAISS)
    cb.create_index(docs)
