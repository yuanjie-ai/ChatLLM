#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : completions
# @Time         : 2023/5/26 13:05
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from fastapi import APIRouter, Body, Depends, HTTPException, Request, status, BackgroundTasks
from fastapi.responses import Response, StreamingResponse, JSONResponse
from sse_starlette import EventSourceResponse

# ME
from meutils.pipe import *
from chatllm.api.config import *
from chatllm.api.datamodels import *
from chatllm.api.routes.responses import *

import json

router = APIRouter()


@router.post("/v1/chat/completions")
async def chat_completions(body: ChatBody, request: Request, background_tasks: BackgroundTasks):
    background_tasks.add_task(torch_gc)
    _id = uuid.uuid1()

    if request.headers.get("Authorization").split(" ")[1] not in tokens:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token is wrong!")

    # if not llm_model: # 空模型
    #     raise HTTPException(status.HTTP_404_NOT_FOUND, "LLM model not found!")

    question = body.messages[-1]
    chat_kwargs = {"temperature": body.temperature, "top_p": body.top_p, "max_tokens": body.max_tokens}

    if question.role == 'user':
        question = question.content
    else:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No Question Found")

    history = []
    user_question = ''
    for message in body.messages:
        if message.role == 'system':
            history.append((message.content, "OK"))
        if message.role == 'user':
            user_question = message.content
        elif message.role == 'assistant':
            assistant_answer = message.content
            history.append((user_question, assistant_answer))

    if debug:  # 日志
        rprint('Request:', json.loads(await request.body()))
        rprint('ChatBody:', body.dict())

    if body.stream:
        def eval_llm():
            first = True
            response = ''  # 方便入库
            for _response in do_chat(question, history=history, **chat_kwargs):
                response += _response
                if first:
                    first = False
                    yield json.dumps(generate_stream_response_start(_id), ensure_ascii=False)
                _ = generate_stream_response(_id, _response)
                yield json.dumps(_, ensure_ascii=False)

            yield json.dumps(generate_stream_response_stop(_id), ensure_ascii=False)
            yield "[DONE]"

            content = generate_response(_id, response)
            content['user'] = body.user
            rprint(content)
            background_tasks.add_task(do_db, pd.DataFrame([content]), 'chatcmpl')

            if debug: logger.success(content)  # 日志

        return EventSourceResponse(eval_llm(), ping=10000)
    else:
        response = ''.join(do_chat(question, history=history, **chat_kwargs))

        content = generate_response(_id, response)
        content['user'] = body.user
        background_tasks.add_task(do_db, pd.DataFrame([content]), 'chatcmpl')

        if debug: logger.success(content)  # 日志

        return JSONResponse(content)


@router.post("/v1/completions")
async def completions(body: CompletionBody, request: Request, background_tasks: BackgroundTasks):
    background_tasks.add_task(torch_gc)

    _id = uuid.uuid1()

    if request.headers.get("Authorization").split(" ")[1] not in tokens:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token is wrong!")

    # if not llm_model: # 空模型
    #     raise HTTPException(status.HTTP_404_NOT_FOUND, "LLM model not found!")

    question = body.prompt
    chat_kwargs = {"temperature": body.temperature, "top_p": body.top_p, "max_tokens": body.max_tokens}

    if debug:  # 日志
        rprint('Request:', json.loads(await request.body()))
        rprint('ChatBody:', body.dict())

    if body.stream:
        def eval_llm():
            response = ''  # 方便入库
            for _response in do_chat(question, **chat_kwargs):
                response += _response
                _ = generate_stream_response(_id, _response, chat=False)
                yield json.dumps(_, ensure_ascii=False)

            yield json.dumps(generate_stream_response_stop(_id, chat=False), ensure_ascii=False)
            yield "[DONE]"

            content = generate_response(_id, response, chat=False)
            content['user'] = body.user
            background_tasks.add_task(do_db, pd.DataFrame([content]), 'cmpl')

            if debug: logger.success(content)  # 日志

        return EventSourceResponse(eval_llm(), ping=10000)
    else:
        response = ''.join(do_chat(question, **chat_kwargs))  # 流式合成

        content = generate_response(_id, response, chat=False)
        content['user'] = body.user
        background_tasks.add_task(do_db, pd.DataFrame([content]), 'cmpl')

        if debug: logger.success(content)  # 日志

        return JSONResponse(content)
