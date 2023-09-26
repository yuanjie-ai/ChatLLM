#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : st_chat
# @Time         : 2023/8/11 14:45
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

import streamlit as st
# st.set_page_config('🔥ChatLLM', layout='wide', initial_sidebar_state='collapsed')

from langchain import LLMChain, PromptTemplate
from langchain.prompts import ChatPromptTemplate

from meutils.pipe import *

from chatllm.llmchain import init_cache
from chatllm.llmchain.applications import ChatFile
from chatllm.llmchain.document_loaders import FileLoader
from chatllm.llmchain.embeddings import OpenAIEmbeddings
from chatllm.llmchain.decorators import llm_stream

from langchain.chat_models import ChatOpenAI
from streamlit_option_menu import option_menu
from meutils.serving.streamlit.common import hide_st_style

hide_st_style()


init_cache(1)

context_prompt_template = """
根据以下信息，简洁、专业地回答用户的问题。如果无法得到答案，请回复：“对不起，根据已知信息无法回答该问题”或“没有提供足够的信息”。请勿编造信息，答案必须使用中文。

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
    assistant_avator="规丞相.png",

    reply_func=lambda input: f'{input}的答案',
    max_turns=3,
    system_prompt="欢迎来找**规丞相**，您有什么要咨询的吗❓"
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

    container1 = st.container()  # 占位符

    prompt = st.chat_input("    🤔 你可以问我任何问题")

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
    else:
        with chat_message(assistant_role):
            message_placeholder = st.empty()
            message_placeholder.markdown(system_prompt, unsafe_allow_html=True)


@st.cache_resource(show_spinner=False)
def get_reply_func(file):
    reply_func = lambda input: f'### ⚠️请先上传文档\n'

    if file:
        docs = FileLoader(file, file.name).load_and_split()
        print(file.name, len(docs))

        cb = ChatFile(embeddings=OpenAIEmbeddings(chunk_size=20), prompt_template=context_prompt_template)
        cb.create_index(docs)
        print(docs)

        reply_func = lambda query: cb.llm_qa(query=query, k=5, threshold=0.5)

    return reply_func


def chatgpt_reply_func():
    template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI bot. Your name is 东北证券“规丞相”. 请牢记你的身份。"),
        ("human", "{user_input}"),
    ])
    llm = LLMChain(llm=ChatOpenAI(streaming=True), prompt=template)
    reply_func = lambda query: llm_stream(llm.run)(query)
    return reply_func


if __name__ == '__main__':
    col1, col2, col3, *_ = st.columns(3)
    with col1:
        st.image('规丞相.png', width=64)
    with col2:
        st.markdown('##### ')
        st.markdown('##### ')
        st.markdown('##### 规丞相驾到')

    st.markdown('> ⚠️“规丞相”仅供东北证券内部测试使用，所做回答不得用于东北证券官方回复。')

    selected = option_menu("", ["开放式问答", "基于知识库问答"], menu_icon="cast", orientation="horizontal")

    reply_func = None
    if selected == '开放式问答':
        st.session_state.messages = []

        reply_func = chatgpt_reply_func()

    else:
        if hasattr(st.session_state, 'messages'):
            st.session_state.messages = []

        file = st.file_uploader(" ", type=['pdf', 'doc', 'docx', 'txt', ], help='目前仅支持单文档问答')
        if file:
            print(f"{time.ctime()}: {file}")

            with st.spinner('AI正在处理...'):
                reply_func = get_reply_func(file)
        else:
            file = open("东北证券股份有限公司合规手册（东证合规发〔2022〕25号 20221229）.pdf", 'rb')
            reply_func = get_reply_func(file)


    chat(reply_func=reply_func)
