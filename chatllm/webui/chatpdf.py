#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chatpdf
# @Time         : 2023/4/25 17:01
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

import streamlit as st
from meutils.pipe import *
from meutils.serving.st_utils import display_pdf, st_chat, set_config

from chatllm.applications.chatpdf import ChatPDF

st.set_page_config(page_title='🔥ChatPDF', layout='wide', initial_sidebar_state='collapsed')


################################################################################################################
class Conf(BaseConfig):
    encode_model = 'nghuyong/ernie-3.0-nano-zh'
    llm = "THUDM/chatglm-6b"  # /Users/betterme/PycharmProjects/AI/CHAT_MODEL/chatglm-6b
    cachedir = 'pdf_cache'

    topk: int = 3
    threshold: float = 0.66


conf = Conf()
conf = set_config(conf)


################################################################################################################


@st.cache_resource()
def qa4pdf(encode_model, model_name_or_path, cachedir):
    qa = ChatPDF(encode_model=encode_model)
    # qa.encode = disk_cache(qa.encode, location=cachedir)  # 缓存
    qa.load_llm(model_name_or_path=model_name_or_path)
    qa.create_index = lru_cache()(qa.create_index)

    return qa


def reply_func(query):
    response = ''
    for _ in qa(query=query, topk=conf.topk, threshold=conf.threshold):
        response += _
        yield response


if st.session_state.get('init'):

    tabs = st.tabs(['ChatPDF', 'PDF文件预览'])

    with tabs[0]:
        file = st.file_uploader("上传PDF", type=['pdf'])
        bytes_array = ''
        try:
            qa = qa4pdf(conf.encode_model, conf.llm, conf.cachedir)
        except Exception as e:
            st.warning('启动前选择正确的参数进行初始化')
            st.error(e)

        if file:
            bytes_array = file.read()
            with st.spinner("构建知识库：文本向量化"):
                qa.create_index(bytes_array)

            base64_pdf = base64.b64encode(bytes_array).decode('utf-8')

            container = st.container()  # 占位符
            text = st.text_area(label="用户输入", height=100, placeholder="请在这儿输入您的问题")

            if st.button("发送", key="predict"):
                with st.spinner("🤔 AI 正在思考，请稍等..."):
                    history = st.session_state.get('state')
                    st.session_state["state"] = st_chat(
                        text, history, container=container,
                        previous_messages=['请上传需要分析的PDF，我将为你解答'],
                        reply_func=reply_func,
                    )

            with st.expander('点击可查看被召回的知识'):
                st.dataframe(qa.recall.drop('embedding', 1, errors='ignore'))
                # st.dataframe(qa.recall)


    with tabs[1]:
        if bytes_array:
            display_pdf(base64_pdf)
        else:
            st.warning('### 请先上传PDF')
