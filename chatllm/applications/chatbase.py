#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : Question2Answer
# @Time         : 2023/4/21 12:25
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.decorators import clear_cuda_cache

from chatllm.utils import DEVICE
from chatllm.llms import load_llm4chat


class ChatBase(object):

    def __init__(self, **kwargs):
        self.do_chat = None

        self.history = []
        self.knowledge_base = None
        self.role = None

        # 重写 chat函数会更好 prompt += "[Round {}]\n问：{}\n答：{}\n".format(i, old_query, response) # 根据角色配置模板
        self.prompt_template = os.getenv('PROMPT_TEMPLATE', '{role}')

    def __call__(self, **kwargs):
        return self.qa(**kwargs)

    def qa(self, query, **kwargs):
        """可重写"""
        return self._qa(query, **kwargs)

    @clear_cuda_cache(bins=int(os.getenv('GPU_TIME_INTERVAL', 2)))  # todo: 异步
    def _qa(self, query, knowledge_base='', role='', max_turns=1, return_history=False):
        self.role = role or os.getenv('LLM_ROLE', '')
        self.knowledge_base = str(knowledge_base).strip()
        if self.knowledge_base:
            self.query = self.prompt_template.format(context=self.knowledge_base, question=query, role='')
        else:
            self.query = """{role}\n基于以上角色，请回答以下问题：{question}""".format(question=query,
                                                                                     role=self.role)  # 知识库为空则转通用回答

        global history
        _history = history[-(max_turns - 1):] if max_turns > 1 else []  # 截取最大轮次
        for _ in self.do_chat(query=self.query.strip(), history=_history, return_history=return_history):
            yield _  # (response, history)

    def load_llm(self, model_name_or_path="THUDM/chatglm-6b", device=DEVICE, **kwargs):
        self.do_chat = load_llm4chat(model_name_or_path, device=device, **kwargs)

    def set_chat_kwargs(self, **kwargs):
        self.do_chat = partial(self.do_chat, **kwargs)


if __name__ == '__main__':
    from chatllm.applications import ChatBase

    qa = ChatBase()
    qa.load_llm(model_name_or_path="/CHAT_MODEL/chatglm-6b")

    for _ in qa(query='你是谁', return_history=False):
        print(_, end='')
