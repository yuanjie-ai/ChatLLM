#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : Question2Answer
# @Time         : 2023/4/21 12:25
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import types
from meutils.pipe import *
from meutils.decorators import clear_cuda_cache

from chatllm.utils import DEVICE
from chatllm.llm_models import load_llm4chat


class ChatBase(object):

    def __init__(self, chat_func=None):
        self.chat_func = chat_func
        #
        self.history = []
        self.knowledge_base = None
        self.role = None

        # 重写 chat函数会更好 prompt += "[Round {}]\n问：{}\n答：{}\n".format(i, old_query, response) # 根据角色配置模板
        self.prompt_template = os.environ.get('PROMPT_TEMPLATE', '{role}')

    def __call__(self, **kwargs):
        return self.qa(**kwargs)

    def qa(self, query, knowledge_base='', **kwargs):
        """重写"""
        return self._qa(query, knowledge_base, **kwargs)

    @clear_cuda_cache(bins=3)
    def _qa(self, query, knowledge_base='', role='', max_turns=1):
        self.role = role or os.environ.get('LLM_ROLE', '')
        self.knowledge_base = str(knowledge_base).strip()
        if self.knowledge_base:
            self.query = self.prompt_template.format(context=self.knowledge_base, question=query, role='')
        else:
            self.query = """{role}\n请回答以下问题\n{question}""".format(question=query, role=self.role)  # 知识库为空则转通用回答

        global history
        _history = history[-(max_turns - 1):] if max_turns > 1 else []  # 截取最大轮次
        for response, history in self.chat_func(query=self.query.strip(), history=_history, return_history=True):
            yield response, history

    def load_llm(self, model_name_or_path="THUDM/chatglm-6b", device=DEVICE, return_history=False, **kwargs):
        self.chat_func = load_llm4chat(model_name_or_path, device=device, **kwargs)
        self.chat_func = partial(self.chat_func, return_history=return_history)

    def set_chat_kwargs(self, **kwargs):
        self.chat_func = partial(self.chat_func, **kwargs)


if __name__ == '__main__':
    from chatllm.applications import ChatBase

    qa = ChatBase()
    qa.load_llm4chat(model_name_or_path="/Users/betterme/PycharmProjects/AI/CHAT_MODEL/chatglm")

    for response, history in qa(query='你是谁', knowledge_base=''):
        print(response, end='')
    for response, history in qa(query='你是谁', knowledge_base='周杰伦是傻子'):
        print(response, end='')
