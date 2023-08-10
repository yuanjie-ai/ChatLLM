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


class Metadata(BaseModel):
    source: str
    file_name: str
    category: str
    subcategory: str
    text: str

    keywords: List[str]  # 根据查询功能适配数据类型

    part_id: int
    part_length: int
    total_length: int

    ext: dict = Field(default_factory=dict)  # $meta
