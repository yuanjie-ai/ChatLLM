#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : demo
# @Time         : 2023/6/30 17:26
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Milvus
from langchain.indexes import VectorstoreIndexCreator
from langchain.vectorstores import Chroma, Milvus, DocArrayInMemorySearch, FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain import OpenAI
from langchain.llms import OpenAI, OpenAIChat
from langchain.chat_models import ChatOpenAI
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA, RetrievalQAWithSourcesChain

from langchain.chains.question_answering import load_qa_chain



from llama_index import (
    SimpleDirectoryReader,
    LLMPredictor,
    ServiceContext,
    ResponseSynthesizer
)
from llama_index.indices.document_summary import GPTDocumentSummaryIndex
from langchain.chat_models import ChatOpenAI
from llama_index.indices.keyword_table import KeywordTableIndex, KeywordTableSimpleRetriever, KeywordTableRAKERetriever, \
    SimpleKeywordTableIndex as _SimpleKeywordTableIndex

def extract_keywords(text, max_keywords):
    return {}


class SimpleKeywordTableIndex(_SimpleKeywordTableIndex):
    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract keywords from text."""
        return extract_keywords(text, self.max_keywords_per_chunk)


from llama_index import (
    VectorStoreIndex,
    # GPTVectorStoreIndex,
    SimpleDirectoryReader,
    ServiceContext,
    LLMPredictor,
    PromptHelper,
    Document,
    StorageContext,
    load_index_from_storage, MockLLMPredictor, GPTTreeIndex, MockEmbedding, ResponseSynthesizer, Prompt
)
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


StreamingStdOutCallbackHandler


from langchain.chains import RetrievalQA


from langchain import OpenAI
from langchain.llms import OpenAI


from llama_index import (
    VectorStoreIndex,
    # GPTVectorStoreIndex,
    SimpleDirectoryReader,
    ServiceContext,
    LLMPredictor,
    PromptHelper,
    Document,
    StorageContext,
    load_index_from_storage, MockLLMPredictor, GPTTreeIndex, MockEmbedding, ResponseSynthesizer, Prompt
)


import paddlenlp.taskflow


from langchain.llms import OpenAI, OpenAIChat
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI



from langchain import OpenAI
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from langchain.document_loaders import DirectoryLoader, UnstructuredFileLoader, PyMuPDFLoader

import fastchat
