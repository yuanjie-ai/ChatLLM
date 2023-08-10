#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : Embeddings
# @Time         : 2023/6/30 17:13
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings



from langchain.chains import ChatVectorDBChain, VectorDBQAWithSourcesChain, ConversationalRetrievalChain, ConversationChain


