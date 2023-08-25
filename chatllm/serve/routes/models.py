#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : models
# @Time         : 2023/7/31 17:00
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from fastapi import APIRouter, Body, Depends, HTTPException
from chatllm.serve.routes.utils import check_api_key
from chatllm.schemas.openai_api_protocol import *

router = APIRouter()

models = []


@router.get("/v1/models", dependencies=[Depends(check_api_key)])
async def show_available_models():
    # TODO: return real model permission details
    model_cards = []
    for m in models:
        model_cards.append(ModelCard(id=m, root=m, permission=[ModelPermission()]))
    return ModelList(data=model_cards)
