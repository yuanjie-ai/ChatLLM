#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : base
# @Time         : 2023/5/26 10:39
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from fastapi import APIRouter, Body, Depends, HTTPException

router = APIRouter()


@router.get("/")
def read_root():
    return {"Hi, baby.": "https://github.com/yuanjie-ai/ChatLLM"}


@router.get("/gpu")
def gpu_info():
    return os.popen("nvidia-smi").read()


@router.get("/v1/models")
def get_models():
    ret = {"data": [], "object": "list"}
    ret['data'].append({
        "created": 1677610602,
        "id": "gpt-3.5-turbo",
        "object": "model",
        "owned_by": "openai",
        "permission": [
            {
                "created": 1680818747,
                "id": "modelperm-fTUZTbzFp7uLLTeMSo9ks6oT",
                "object": "model_permission",
                "allow_create_engine": False,
                "allow_sampling": True,
                "allow_logprobs": True,
                "allow_search_indices": False,
                "allow_view": True,
                "allow_fine_tuning": False,
                "organization": "*",
                "group": None,
                "is_blocking": False
            }
        ],
        "root": "gpt-3.5-turbo",
        "parent": None,
    })
    ret['data'].append({
        "created": 1671217299,
        "id": "text-embedding-ada-002",
        "object": "model",
        "owned_by": "openai-internal",
        "permission": [
            {
                "created": 1678892857,
                "id": "modelperm-Dbv2FOgMdlDjO8py8vEjD5Mi",
                "object": "model_permission",
                "allow_create_engine": False,
                "allow_sampling": True,
                "allow_logprobs": True,
                "allow_search_indices": True,
                "allow_view": True,
                "allow_fine_tuning": False,
                "organization": "*",
                "group": None,
                "is_blocking": False
            }
        ],
        "root": "text-embedding-ada-002",
        "parent": ""
    })

    return ret
