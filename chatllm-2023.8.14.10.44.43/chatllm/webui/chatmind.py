#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chatmind
# @Time         : 2023/6/29 15:24
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from chatllm.applications.chatmind import ChatMind

import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title='🔥ChatMind', layout='wide', initial_sidebar_state='collapsed')

api_key = st.sidebar.text_input('API_KEY', 'sk-...')

os.environ['API_KEY'] = api_key
qa = ChatMind()
qa.load_llm()

with st.form('form'):
    title = st.text_input("输入主题", value='人工智能的未来')
    col1, col2 = st.columns(2)
    context: str = ''
    with col1:
        if st.form_submit_button("🚀开始创作"):
            output = st.empty()
            for i in qa(title=title):
                context += i
                output.markdown(context)
    with col2:
        if context:
            html_str = qa.mind_html(context)

            html(html_str, height=1000)
