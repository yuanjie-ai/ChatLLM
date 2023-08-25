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
from chatllm.llmchain.embeddings import OpenAIEmbeddings
from chatllm.llmchain.document_loaders import FilesLoader

from langchain.text_splitter import *
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.base import Embeddings


class ChatBase(object):

    def __init__(self,
                 model: str = "gpt-3.5-turbo-16k-0613", temperature: float = 0,
                 collection_name: str = 'TEST', chunk_size: int = 5,
                 get_api_key: Optional[Callable[[int], List[str]]] = None,
                 ):
        self.collection_name = collection_name
        # 根据 model 选择 llm/openai_api_base
        self.llm = ChatOpenAI(model=model, temperature=np.clip(temperature, 0, 1), streaming=True)
        self.embeddings = OpenAIEmbeddings(chunk_size=chunk_size)  # todo: 可选
        if get_api_key:
            self.embeddings.get_api_key = get_api_key
            self.embeddings.openai_api_key = get_api_key(1)[0]
            self.llm.openai_api_key = get_api_key(1)[0]

        self.chain = load_qa_chain(self.llm, chain_type="stuff")

        # self.chain.llm_chain.prompt.messages[0].prompt.template = \
        #     f'System time: {datetime.datetime.now()};' \
        #     + self.chain.llm_chain.prompt.messages[0].prompt.template

        _vdb_kwargs = self.vdb_kwargs.copy()
        _vdb_kwargs['embedding_function'] = _vdb_kwargs.pop('embedding')
        self.vdb: Optional[Milvus] = Milvus(**_vdb_kwargs)

    def pipeline(self):
        pass

    def llm_qa(self, query: str, k: int = 5, threshold: float = 0.5, **kwargs: Any):
        """todo: pipeline"""
        docs = self.vdb.similarity_search(query, k=max(k, 10), threshold=threshold, **kwargs)
        docs = docs | xUnique_plus(lambda doc: doc.page_content.strip())  # 按内容去重，todo: 按语义相似度去重
        docs = docs[:k]
        # todo: 上下文信息
        docs = [Document(page_content=f"system time: {datetime.datetime.now()}")] + docs
        if docs:
            # chain.run(input_documents=docs, question=query)
            return llm_stream(self.chain.run)({"input_documents": docs, "question": query})

    @staticmethod
    def load_file(file_paths, chunk_size=2000, chunk_overlap=200, **kwargs):
        """支持多文件"""
        loader = FilesLoader(file_paths)
        docs = loader.load_and_split(
            RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, add_start_index=True)
        )
        return docs

    @diskcache(location=os.getenv('INSERT_VECTOR_CACHE', '~/.cache/insert_vector_cache'), ignore=['self'])
    def create_index(self, docs: List[Document], **kwargs):
        """初始化 drop_old=True"""
        self.vdb = Milvus.from_documents(docs, **{**self.vdb_kwargs, **kwargs})

    @cached_property
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
