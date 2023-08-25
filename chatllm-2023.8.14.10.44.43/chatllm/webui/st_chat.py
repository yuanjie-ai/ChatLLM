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
            st.markdown(message.content, unsafe_allow_html=True)

    if prompt := st.chat_input("    🔥请提问？"):
        print(prompt)

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
            message_placeholder.markdown(response, unsafe_allow_html=True)

        # Add robot response to chat history
        st.session_state.messages.append(ChatMessage(role=assistant_role, content=response))


@lru_cache()
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


@st.cache_resource
def get_embeddings():
    model_name = '/Users/betterme/PycharmProjects/AI/m3e-small'
    encode_kwargs = {'normalize_embeddings': True, "show_progress_bar": True}
    embeddings = HuggingFaceEmbeddings(model_name=model_name, encode_kwargs=encode_kwargs)
    return embeddings


if __name__ == '__main__':
    st.markdown('# 📔基于本地知识库问答')
    source = """
    <details markdown="1">
        <summary>详情</summary>

- [ ] 功能点
    - [x] 接入非结构化文档（已支持 pdf、docx 文件格式）
    - [ ] 增加多级缓存缓存

    </details>
    """.strip()
    reply_func = lambda input: f'### ⚠️请先上传文档\n' + source

    file = st.file_uploader("Choose a file", type=['pdf'], help='目前仅支持单文档问答')
    if file:
        from chatllm.llmchain.applications import ChatBase
        from chatllm.llmchain.embeddings import HuggingFaceEmbeddings
        from chatllm.llmchain.vectorstores import FAISS
        from chatllm.llmchain.llms import SparkBot
        from chatllm.llmchain import init

        init()

        bytes_array = file.read()
        docs = bytes2docs(bytes_array)

        llm = SparkBot()
        embeddings = get_embeddings()
        faiss = FAISS.from_documents(docs, embeddings)

        cb = ChatBase(llm=llm, embeddings=embeddings, vectorstore_cls=FAISS)
        cb.create_index(docs)

        for i in cb.llm_qa('你好'):
            print(i, end='')

        reply_func = lambda query: cb.llm_qa(query=query)

    chat(reply_func=reply_func)
