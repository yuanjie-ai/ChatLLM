#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chatpdf
# @Time         : 2023/4/25 17:01
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from chatllm.applications import ChatBase
from chatllm.utils import load_llm4chat

import streamlit as st
from appzoo.streamlit_app.utils import display_pdf, reply4input

st.set_page_config('🔥ChatLLM', layout='centered', initial_sidebar_state='collapsed')


@st.cache_resource
def get_chat_func():
    chat_func = load_llm4chat(
        model_name_or_path="/CHAT_MODEL/chatglm-6b"
    )
    return chat_func


chat_func = get_chat_func()

qa = ChatBase(chat_func=chat_func)


def reply_func(query):
    for response, _ in qa(query=query):
        yield response


# def reply_func(x):
#     for i in range(10):
#         time.sleep(1)
#         x += str(i)
#         yield x


container = st.container()  # 占位符
text = st.text_area(label="用户输入", height=100, placeholder="请在这儿输入您的问题")
# knowledge_base = st.sidebar.text_area(label="知识库", height=100, placeholder="请在这儿输入您的问题")

if st.button("发送", key="predict"):
    with st.spinner("AI正在思考，请稍等........"):
        history = st.session_state.get('state')
        st.session_state["state"] = reply4input(text, history, container=container, reply_func=reply_func)
