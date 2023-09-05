#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2023/7/13 08:53
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *

from langchain.callbacks import AsyncIteratorCallbackHandler, OpenAICallbackHandler
from chatllm.llmchain.callbacks import StreamingGeneratorCallbackHandler


@decorator
def llm_stream(func, *args, **kwargs):
    """
    for i in llm_stream(llm.predict)('周杰伦是谁'):
        print(i, end='')
    """
    handler = StreamingGeneratorCallbackHandler()

    kwargs['callbacks'] = [handler]

    # from threading import Thread
    # thread = Thread(target=func, args=args, kwargs=kwargs)
    # thread.start()

    background_task(func)(*args, **kwargs)
    return handler.get_response_gen()


@decorator
async def llm_astream(func, *args, **kwargs):
    """
    async for i in llm_astream(llm.apredict)('周杰伦是谁'):
        print(i, end='')
    """
    handler = AsyncIteratorCallbackHandler()
    kwargs['callbacks'] = [handler]

    task = asyncio.create_task(func(*args, **kwargs))
    async for token in handler.aiter():
        yield token


@decorator
async def llm_astream(func, *args, **kwargs):
    """
    async for i in llm_astream(llm.apredict)('周杰伦是谁'):
        print(i, end='')
    """
    handler = AsyncIteratorCallbackHandler()
    kwargs['callbacks'] = [handler]

    task = asyncio.create_task(func(*args, **kwargs))
    async for token in handler.aiter():
        yield token


if __name__ == '__main__':
    from langchain.chat_models import ChatOpenAI

    llm = ChatOpenAI(streaming=True, temperature=0)  # 很重要：streaming=True

    # with timer('stream'):
    #     for i in llm_stream(llm.predict)('周杰伦是谁'):
    #         print(i, end='')
    #
    # with timer('老异步请求'):
    #     async def main():
    #         print('\n####################异步####################\n')
    #         async for i in llm_astream(llm.apredict)('周杰伦是谁'):
    #             print(i, end='')
    #
    #
    #     asyncio.run(main())

    with timer('新异步请求'):
        gen = llm_astream(llm.apredict)('周杰伦是谁')
        for i in async2sync_generator(gen):
            print(i, end='')
