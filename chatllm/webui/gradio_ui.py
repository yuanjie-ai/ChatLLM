#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : gradio_ui
# @Time         : 2023/4/24 18:57
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

import gradio as gr
import mdtex2html

########################################################################
from chatllm.utils import llm_load, load_llm4chat
from chatllm.applications import Chat

MODEL = '/Users/betterme/PycharmProjects/AI/CHAT_MODEL/chatglm'

chat_func = load_llm4chat(MODEL, device='mps')

qa = Chat(chat_func)
########################################################################
"""Override Chatbot.postprocess"""


def postprocess(self, y):
    if y is None:
        return []
    for i, (message, response) in enumerate(y):
        y[i] = (
            None if message is None else mdtex2html.convert((message)),
            None if response is None else mdtex2html.convert(response),
        )
    return y


gr.Chatbot.postprocess = postprocess


def parse_text(text):
    """copy from https://github.com/GaiZhenbiao/ChuanhuChatGPT/"""
    lines = text.split("\n")
    lines = [line for line in lines if line != ""]
    count = 0
    for i, line in enumerate(lines):
        if "```" in line:
            count += 1
            items = line.split('`')
            if count % 2 == 1:
                lines[i] = f'<pre><code class="language-{items[-1]}">'
            else:
                lines[i] = f'<br></code></pre>'
        else:
            if i > 0:
                if count % 2 == 1:
                    line = line.replace("`", "\`")
                    line = line.replace("<", "&lt;")
                    line = line.replace(">", "&gt;")
                    line = line.replace(" ", "&nbsp;")
                    line = line.replace("*", "&ast;")
                    line = line.replace("_", "&lowbar;")
                    line = line.replace("-", "&#45;")
                    line = line.replace(".", "&#46;")
                    line = line.replace("!", "&#33;")
                    line = line.replace("(", "&#40;")
                    line = line.replace(")", "&#41;")
                    line = line.replace("$", "&#36;")
                lines[i] = "<br>" + line
    text = "".join(lines)
    return text


def predict(input, chatbot, max_length, top_p, temperature, history, knowledge_base=''):
    chatbot.append((parse_text(input), ""))

    qa.set_chat_kwargs(max_length=max_length, top_p=top_p, temperature=temperature)

    for response, history in qa(query=input, knowledge_base=knowledge_base):
        chatbot[-1] = (parse_text(input), parse_text(response))
        yield chatbot, history


def reset_user_input():
    return gr.update(value='')


def reset_state():
    return [], []


with gr.Blocks() as demo:
    gr.HTML("""<h1 align="center">LLM4CHAT</h1>""")

    chatbot = gr.Chatbot()
    with gr.Row():
        with gr.Column(scale=4):
            # with gr.Column(scale=2):
            #     knowledge_base = gr.Textbox(show_label=False, placeholder="输入知识", lines=10).style(container=False)
            with gr.Column(scale=12):
                user_input = gr.Textbox(show_label=False, placeholder="输入问题", lines=20).style(container=False)
            with gr.Column(min_width=32, scale=1):
                submitBtn = gr.Button("Submit", variant="primary")
        with gr.Column(scale=1):
            emptyBtn = gr.Button("Clear History")
            max_length = gr.Slider(0, 4096, value=2048, step=1.0, label="Maximum length", interactive=True)
            top_p = gr.Slider(0, 1, value=0.7, step=0.01, label="Top P", interactive=True)
            temperature = gr.Slider(0, 1, value=0.95, step=0.01, label="Temperature", interactive=True)

            knowledge_base = gr.Textbox(label='📚知识库', placeholder="输入知识", lines=10).style(container=False)

    history = gr.State([])

    submitBtn.click(predict, [user_input, chatbot, max_length, top_p, temperature, history, knowledge_base],
                    [chatbot, history],
                    show_progress=True)
    submitBtn.click(reset_user_input, [], [user_input])

    emptyBtn.click(reset_state, outputs=[chatbot, history], show_progress=True)

demo.queue().launch(share=False, inbrowser=True, debug=True)
