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


def generate_response(id, content: str, chat: bool = True):
    # 客户端会更新这些值
    _time = int(time.time())

    if chat:
        return {
            "id": f"chatcmpl-{id}",
            "object": "chat.completion",
            "created": _time,
            "model": "gpt-3.5-turbo-0301",
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
            },
            "choices": [
                {
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop", "index": 0
                }
            ]
        }
    else:
        return {
            "id": f"cmpl-{id}",
            "object": "text_completion",
            "created": _time,
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


def generate_stream_response_start(id):
    _time = int(time.time())

    return {
        "id": f"chatcmpl-{id}",
        "object": "chat.completion.chunk",
        "created": _time,
        "model": "gpt-3.5-turbo-0301",
        "choices": [{"delta": {"role": "assistant"}, "index": 0, "finish_reason": None}]
    }


def generate_stream_response(id, content: str, chat: bool = True):
    _time = int(time.time())

    if chat:
        return {
            "id": f"chatcmpl-{id}",  # TODO
            "object": "chat.completion.chunk",
            "created": _time,
            "model": "gpt-3.5-turbo-0301",
            "choices": [{"delta": {"content": content}, "index": 0, "finish_reason": None}]
        }
    else:
        return {
            "id": f"cmpl-{id}",
            "object": "text_completion",
            "created": _time,
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


def generate_stream_response_stop(id, chat: bool = True):
    _time = int(time.time())

    if chat:
        return {
            "id": f"chatcmpl-{id}",
            "object": "chat.completion.chunk",
            "created": _time,
            "model": "gpt-3.5-turbo-0301",
            "choices": [{"delta": {}, "index": 0, "finish_reason": "stop"}]
        }
    else:
        return {
            "id": f"cmpl-{id}",
            "object": "text_completion",
            "created": _time,
            "choices": [
                {"text": "", "index": 0, "logprobs": None, "finish_reason": "stop"}],
            "model": "text-davinci-003",
        }



if __name__ == '__main__':
    print(generate_stream_response(''))
