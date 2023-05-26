#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : stream_response
# @Time         : 2023/5/26 14:46
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *


def generate_response(content: str, chat: bool = True):
    if chat:
        return {
            "id": "chatcmpl-77PZm95TtxE0oYLRx3cxa6HtIDI7s",
            "object": "chat.completion",
            "created": 1682000966,
            "model": "gpt-3.5-turbo-0301",
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
            },
            "choices": [{
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop", "index": 0}
            ]
        }
    else:
        return {
            "id": "cmpl-uqkvlQyYK7bGYrRHQ0eXlWi7",
            "object": "text_completion",
            "created": 1589478378,
            "model": "text-davinci-003",
            "choices": [
                {
                    "text": content,
                    "index": 0,
                    "logprobs": None,
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }
        }


def generate_stream_response_start():
    return {
        "id": "chatcmpl-77QWpn5cxFi9sVMw56DZReDiGKmcB",
        "object": "chat.completion.chunk", "created": 1682004627,
        "model": "gpt-3.5-turbo-0301",
        "choices": [{"delta": {"role": "assistant"}, "index": 0, "finish_reason": None}]
    }


def generate_stream_response(content: str, chat: bool = True):
    if chat:
        return {
            "id": "chatcmpl-77QWpn5cxFi9sVMw56DZReDiGKmcB",
            "object": "chat.completion.chunk",
            "created": 1682004627,
            "model": "gpt-3.5-turbo-0301",
            "choices": [{"delta": {"content": content}, "index": 0, "finish_reason": None}
                        ]}
    else:
        return {
            "id": "cmpl-7GfnvmcsDmmTVbPHmTBcNqlMtaEVj",
            "object": "text_completion",
            "created": 1684208299,
            "choices": [
                {
                    "text": content,
                    "index": 0,
                    "logprobs": None,
                    "finish_reason": None,
                }
            ],
            "model": "text-davinci-003"
        }


def generate_stream_response_stop(chat: bool = True):
    if chat:
        return {"id": "chatcmpl-77QWpn5cxFi9sVMw56DZReDiGKmcB",
                "object": "chat.completion.chunk", "created": 1682004627,
                "model": "gpt-3.5-turbo-0301",
                "choices": [{"delta": {}, "index": 0, "finish_reason": "stop"}]
                }
    else:
        return {
            "id": "cmpl-7GfnvmcsDmmTVbPHmTBcNqlMtaEVj",
            "object": "text_completion",
            "created": 1684208299,
            "choices": [
                {"text": "", "index": 0, "logprobs": None, "finish_reason": "stop"}],
            "model": "text-davinci-003",
        }


if __name__ == '__main__':
    print(generate_stream_response(''))
