#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : st_chat
# @Time         : 2023/8/11 14:45
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *

import streamlit as st


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
            st.markdown(message.content)

    if prompt := st.chat_input("    🔥请提问？"):
        # Display user message in chat message container
        with chat_message(user_role):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append(ChatMessage(role=user_role, content=prompt))

        with chat_message(assistant_role):
            message_placeholder = st.empty()

            response = ''
            for token in reply_func(prompt):
                # Display robot response in chat message container
                response += token
                message_placeholder.markdown(response + "▌")
            message_placeholder.markdown(response)

        # Add robot response to chat history
        st.session_state.messages.append(ChatMessage(role=assistant_role, content=response))


def bytes2docs(bytes_array):
    from meutils.office_automation.pdf import extract_text
    from langchain.text_splitter import RecursiveCharacterTextSplitter, Document

    separators = ['\n\n', '\r', '\n', '\r\n', '。', '!', '！', '\\?', '？', '……', '…']
    textsplitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=0,
        add_start_index=True,
        separators=separators
    )
    text = extract_text(bytes_array)
    docs = textsplitter.split_documents([Document(page_content=text)])
    return docs


if __name__ == '__main__':
    st.markdown('# 📔基于本地知识库问答')
    reply_func = lambda input: f'# ⚠️请先上传文档'

    file = st.file_uploader("Choose a file", type=['pdf', 'docx'], help='目前仅支持单文档问答')
    if file:
        bytes_array = file.read()
        docs = bytes2docs(bytes_array)

        from chatllm.llmchain.applications import ChatBase

        cb = ChatBase(collection_name='NESC')
        cb.create_index(docs)
        reply_func = cb.llm_qa

    chat(reply_func=reply_func)
