#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : st_chat
# @Time         : 2023/8/11 14:45
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import time

import streamlit as st

from meutils.pipe import *

from chatllm.llmchain import init_cache
from chatllm.llmchain.applications import ChatFile
from chatllm.llmchain.document_loaders import FileLoader
from chatllm.llmchain.embeddings import OpenAIEmbeddings
from chatllm.llmchain.prompts.prompt_templates import CHAT_CONTEXT_PROMPT_WITH_SOURCE

init_cache(1)

context_prompt_template = """
根据以下信息，简洁、专业地回答用户的问题。如果无法得到答案，请回复：“根据已知信息无法回答该问题”或“没有提供足够的信息”。请勿编造信息，答案必须使用中文。

已知信息：
{context}

问题：
{question}

让我们一步一步思考并回答：
""".strip()  # Let's think step by step


class ChatMessage(BaseModel):
    role: str
    content: str


def chat(
    user_role='user',

    assistant_role='assistant',
    assistant_avator="nesc.jpeg",

    reply_func=lambda input: f'{input}的答案',
    max_turns=3,
):
    def chat_message(role):
        if role == 'user':
            return st.chat_message(user_role)
        else:
            return st.chat_message(assistant_role, avatar=assistant_avator)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    else:
        st.session_state.messages = st.session_state.messages[-2 * (max_turns - 1):]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with chat_message(message.role):
            st.markdown(message.content, unsafe_allow_html=True)

    prompt = st.chat_input("    🔥请提问？")
    if prompt:
        print('\n')
        print(prompt)
        prompt = prompt.strip()
        # Display user message in chat message container
        with chat_message(user_role):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append(ChatMessage(role=user_role, content=prompt))

        with chat_message(assistant_role):
            message_placeholder = st.empty()

            response = ''
            gen = reply_func(prompt) or '根据已知信息无法召回相关内容。'
            for token in gen:
                # Display robot response in chat message container
                response += token
                message_placeholder.markdown(response + "▌")
            message_placeholder.markdown(response, unsafe_allow_html=True)

        # Add robot response to chat history
        st.session_state.messages.append(ChatMessage(role=assistant_role, content=response))


@st.cache_resource
def get_reply_func(file):
    if file:
        docs = FileLoader(file, file.name).load_and_split()
        print(file.name, len(docs))
        from chatllm.llmchain.vectorstores import Milvus, FAISS

        cb = ChatFile(embeddings=OpenAIEmbeddings(chunk_size=20), prompt_template=context_prompt_template)
        cb.create_index(docs)

        reply_func = lambda query: cb.llm_qa(query=query, k=5, threshold=0.5)

        return reply_func

    source = """
        <details markdown="1">
            <summary>详情</summary>

    - [ ] 功能点
        - [x] 接入非结构化文档（已支持 pdf、docx 文件格式）
        - [ ] 增加多级缓存缓存

        </details>
        """.strip()

    reply_func = lambda input: f'### ⚠️请先上传文档\n' + source
    return reply_func


if __name__ == '__main__':
    st.markdown('# 📔基于本地知识库问答')

    file = st.file_uploader("Choose a file", type=['pdf', 'doc', 'docx', 'txt', ], help='目前仅支持单文档问答')
    print(f"{time.ctime()}: {file}")
    with st.spinner('AI正在处理...'):
        reply_func = get_reply_func(file)

        chat(reply_func=reply_func)
