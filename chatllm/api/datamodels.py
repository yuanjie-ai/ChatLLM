#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : datamodel
# @Time         : 2023/5/25 18:29
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *


class Message(BaseModel):
    role: str
    content: str


class ChatBody(BaseModel):
    messages: List[Message]
    model: str
    stream: Optional[bool] = False
    max_tokens: Optional[int]
    temperature: Optional[float]
    top_p: Optional[float]


class CompletionBody(BaseModel):
    prompt: str
    model: str
    stream: Optional[bool] = False
    max_tokens: Optional[int]
    temperature: Optional[float]
    top_p: Optional[float]


class EmbeddingsBody(BaseModel):
    # Python 3.8 does not support str | List[str]
    input: Any
    model: Optional[str]
