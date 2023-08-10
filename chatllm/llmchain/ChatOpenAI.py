#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ChatOpenAI
# @Time         : 2023/7/4 13:54
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 异步流式输出 https://github.com/sugarforever/LangChain-Tutorials/blob/main/StreamChat/app.py

# from langchain.callbacks import AsyncIteratorCallbackHandler
# callback = AsyncIteratorCallbackHandler()
# model = ChatOpenAI(streaming=True, verbose=True, callbacks=[callback])
# coroutine = model.agenerate(messages=[[HumanMessage(content='1+111')]])
# task = asyncio.create_task(coroutine)
# async for token in callback.aiter():
#     print(f"{token}", end='')

from meutils.pipe import *
from langchain.chat_models import ChatOpenAI as _ChatOpenAI
from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler

from langchain.chains import ConversationalRetrievalChain, VectorDBQAWithSourcesChain, RetrievalQAWithSourcesChain, RetrievalQA, MultiRetrievalQAChain



from langchain.memory import ConversationBufferMemory
from langchain.chains.conversation.memory import ConversationSummaryMemory


#
# qa = RetrievalQA.from_chain_type(
#     llm=llm, chain_type="stuff",
#     retriever=retriever1,
#     return_source_documents=True, memory=memory
# )
