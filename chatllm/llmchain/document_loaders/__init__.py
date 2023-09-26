#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : __init__.py
# @Time         : 2023/6/30 18:47
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :


from chatllm.llmchain.document_loaders.text import TextLoader
from chatllm.llmchain.document_loaders.pdf import PyMuPDFLoader
from chatllm.llmchain.document_loaders.docx import Docx2txtLoader
from chatllm.llmchain.document_loaders.image import UnstructuredImageLoader  # 依赖 nltk

from chatllm.llmchain.document_loaders.file import FileLoader
from chatllm.llmchain.document_loaders.FilesLoader import FilesLoader
