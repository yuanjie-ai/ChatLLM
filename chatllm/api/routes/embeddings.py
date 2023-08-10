#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : embeddings
# @Time         : 2023/5/26 10:44
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from fastapi import APIRouter, Body, Depends, HTTPException, Request, status, BackgroundTasks
from fastapi.responses import JSONResponse

# ME
from meutils.pipe import *
from chatllm.api.config import *
from chatllm.api.datamodels import *

router = APIRouter()


def do_embeddings(body: EmbeddingsBody, request: Request, background_tasks: BackgroundTasks):
    background_tasks.add_task(torch_gc)

    if request.headers.get("Authorization").split(" ")[1] not in tokens:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token is wrong!")

    if not embeddings_model:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Embeddings model not found!")

    texts = body.input
    if isinstance(texts, str):
        texts = [texts]

    embeddings = embedding_model.encode(texts)

    data = []
    for i, embed in enumerate(embeddings):
        data.append({
            "object": "embedding",
            "index": i,
            "embedding": embed.tolist(),
        })
    content = {
        "object": "list",
        "data": data,
        "model": "text-embedding-ada-002-v2",
        "usage": {
            "prompt_tokens": 0,
            "total_tokens": 0
        }
    }
    return JSONResponse(status_code=200, content=content)


@router.post("/v1/embeddings")
async def embeddings(body: EmbeddingsBody, request: Request, background_tasks: BackgroundTasks):
    return do_embeddings(body, request, background_tasks)


@router.post("/v1/engines/{engine}/embeddings")
async def engines_embeddings(engine: str, body: EmbeddingsBody, request: Request, background_tasks: BackgroundTasks):
    return do_embeddings(body, request, background_tasks)
