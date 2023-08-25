#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : api
# @Time         : 2023/5/26 14:56
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from fastapi import APIRouter

from chatllm.api.routes import base, completions, embeddings

router = APIRouter()
router.include_router(base.router, tags=["baseinfo"])
router.include_router(completions.router, tags=["completions"])
router.include_router(embeddings.router, tags=["embeddings"])


