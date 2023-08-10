#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chatmind
# @Time         : 2023/5/4 11:46
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://mp.weixin.qq.com/s/gbqd8bzKRbbOqf5ebHICWg

from chatllm.llms import load_llm4chat
from meutils.pipe import *


class ChatMind(object):

    def __init__(self):
        role = """
        请扮演为一个思维导图制作者，必须使用中文回答。
        要求：
        1. 根据《》中的主题创作
        2. 输出格式为markdown: "# "表示中央主题， "## "表示主要主题，"### "表示子主题，"- "表示叶子节点"
        3. 包含多个主题和子主题，以及叶子节点。
        4. 叶子节点内容长度10-50
        """
        self.history = [
            {"role": "system", "content": role},
        ]

    def __call__(self, **kwargs):
        return self.qa(**kwargs)

    def qa(self, title, **kwargs):
        return self.do_chat(f"《{title}》", history=self.history)

    def load_llm(self, model_name_or_path="chatgpt", **kwargs):
        self.do_chat = load_llm4chat(model_name_or_path, **kwargs)

    def set_chat_kwargs(self, **kwargs):
        self.do_chat = partial(self.do_chat, **kwargs)

    def mind_html(self, md='# Title\n ## SubTitle\n - Node'):
        # 后处理
        md = re.sub(r'(?m)^(?![\-#]).+', '\n', md) # 仅保留 # - 开头

        from jinja2 import Template, Environment, PackageLoader, FileSystemLoader

        env = Environment(loader=PackageLoader('meutils'))
        template = env.get_template('markmap.html')
        return template.render(md=md)
