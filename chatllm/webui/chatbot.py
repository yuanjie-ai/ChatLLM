#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chatllm
# @Time         : 2023/9/21 16:05
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://nicedouble-streamlitantdcomponentsdemo-app-middmy.streamlit.app/

from meutils.pipe import *
import streamlit as st
import streamlit_antd_components as sac

# sidebar
with st.sidebar:
    sac.divider(label='Chatllm', icon='chat-dots-fill', align='center', dashed=False, bold=True, key='start')
    with st.columns(3)[1]:
        st.image('logo.png', caption='LOGO', use_column_width=True)
    # st.info('这是一个logo', icon='🔥')

    sac.divider(label='知识库', icon='database', align='center', dashed=True, bold=True)
    item = sac.tree(
        label='**知识库**', index=0, format_func='title', icon='database', checkbox=True,
        items=[
            sac.TreeItem(
                '语文', tag=sac.Tag('tag', color='red', bordered=True), tooltip='item1 tooltip',
                children=[sac.TreeItem('古诗词')]
            ),

            sac.TreeItem(
                '数学',
                children=[sac.TreeItem('高数'), sac.TreeItem('线性代数')]
            ),

            sac.TreeItem('item2', icon='apple', tooltip='item2 tooltip', children=[
                sac.TreeItem('item2-1', icon='github', tag='tag0'),
                sac.TreeItem('item2-2', children=[
                    sac.TreeItem('item2-2-1'),
                    sac.TreeItem('item2-2-2'),
                    sac.TreeItem('item2-2-3', children=[
                        sac.TreeItem('item2-2-3-1'),
                        sac.TreeItem('item2-2-3-2'),
                        sac.TreeItem('item2-2-3-3'),
                    ]),
                ]),
            ]),
            sac.TreeItem('disabled', disabled=True),
            sac.TreeItem('item3', children=[
                sac.TreeItem('item3-1'),
                sac.TreeItem('item3-2'),
                sac.TreeItem('text' * 30),
            ]),
        ])

    st.markdown(f'Item: {item}')

# 正文
sac.alert(message='**这是一段广告**', icon=True, banner=True)

sac.segmented(
    items=[
        sac.SegmentedItem(icon='fire'),
        sac.SegmentedItem(icon='apple'),
        sac.SegmentedItem(icon='wechat'),
        sac.SegmentedItem(icon='chat-dots-fill'),
        sac.SegmentedItem(icon='book-half'),
        sac.SegmentedItem(icon='file-earmark-pdf-fill'),

        sac.SegmentedItem(icon='filetype-pdf'),
        sac.SegmentedItem(icon='filetype-docx'),
        sac.SegmentedItem(icon='filetype-txt'),

        sac.SegmentedItem(label='github', icon='github'),
        sac.SegmentedItem(label='link', icon='link', href='https://mantine.dev/core/segmented-control/'),
        sac.SegmentedItem(label='disabled', disabled=True),
    ],
    format_func='title', radius='xl', size='xs', grow=True
)

cols = st.columns(2)
with cols[0]:
    with st.chat_message('user'):
        st.markdown('user1')
    with st.chat_message('assistant'):
        st.markdown('assistant1')

with cols[1]:
    with st.chat_message('user'):
        st.markdown('user2')
    with st.chat_message('assistant'):
        st.markdown('assistant2')

# 最下面
st.chat_input()  # `st.chat_input()` can't be used inside an `st.expander`, `st.form`, `st.tabs`, `st.columns`, or `st.sidebar`.
