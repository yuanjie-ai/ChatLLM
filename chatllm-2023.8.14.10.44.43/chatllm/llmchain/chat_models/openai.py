#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : callbacks
# @Time         : 2023/7/12 17:37
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
from threading import Thread

from langchain.chat_models import ChatOpenAI as _ChatOpenAI
from langchain.callbacks import AsyncIteratorCallbackHandler
from chatllm.llmchain.callbacks import StreamingGeneratorCallbackHandler

from meutils.pipe import *

# llm._get_llm_string()
class ChatOpenAI(_ChatOpenAI):

    def stream(self, text: str, *, stop: Optional[Sequence[str]] = None, **kwargs: Any) -> Generator:
        """Stream the answer to a query.

        NOTE: this is a beta feature. Will try to build or use
        better abstractions about response handling.

        """
        # if self.cache: return iter(self.predict(text, stop=stop, **kwargs)) # 在外面做缓存逻辑

        handler = StreamingGeneratorCallbackHandler()
        self.callbacks = [handler]
        self.streaming = True

        #  background_tasks.add_task(_predict, text, **kwargs)
        kwargs['stop'] = stop
        thread = Thread(target=self.predict, args=[text], kwargs=kwargs)
        thread.start()  # thread.is_alive() 瞬间完成从缓存里取

        return handler.get_response_gen()

    async def astream(self, text: str, *, stop: Optional[Sequence[str]] = None, **kwargs: Any) -> AsyncGenerator:
        handler = AsyncIteratorCallbackHandler()
        self.callbacks = [handler]
        self.streaming = True

        task = asyncio.create_task(self.apredict(text, stop=stop, **kwargs))

        async for token in handler.aiter():
            yield token



if __name__ == '__main__':
    llm = ChatOpenAI(streaming=True, temperature=0)
    for i in llm.stream('你好'):
        print(i, end='')

    async for token in llm.astream('你好'):
        print(token, end='')
