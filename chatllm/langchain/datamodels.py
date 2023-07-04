#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : datamodels
# @Time         : 2023/6/30 18:23
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import numpy as np

from meutils.pipe import *


class Document(BaseModel):
    page_content: str
    doc_embedding: np.array
    page_embedding: np.array
    page_importance: float

    metadata: dict = Field(default_factory=dict)

