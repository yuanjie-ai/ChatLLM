#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : Loader
# @Time         : 2023/6/30 17:13
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *

from langchain.document_loaders import OnlinePDFLoader
from langchain.document_loaders import PyMuPDFLoader

from langchain.document_transformers import EmbeddingsRedundantFilter  # 过滤相似文档
