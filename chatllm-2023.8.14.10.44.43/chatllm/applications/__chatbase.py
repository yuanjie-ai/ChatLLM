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

from chatllm.utils import DEVICE, load_llm4chat


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

    def set_chat_kwargs(self, **kwargs):
        self.chat_func = partial(self.chat_func, **kwargs)

    @clear_cuda_cache(bins=3)
    def _qa(self, query, knowledge_base='', role='', max_turns=1):
        self.role = role or os.environ.get('LLM_ROLE', '')
        self.knowledge_base = str(knowledge_base).strip()
        if self.knowledge_base:
            query = self.prompt_template.format(context=self.knowledge_base, question=query, role=' ').strip()  # 无角色扮演
        else:
            query = """{role}\n{question}""".format(question=query, role=self.role).strip()  # 知识库为空则转通用回答

        self.query = query

        _history = self.history[-(max_turns - 1):] if max_turns > 1 else []
        result = self.chat_func(query=query, history=_history)

        if isinstance(result, types.GeneratorType):
            return self._stream(result)
        else:
            response, history = result
            # self.history_ = history  # 历史所有
            self.history += [[None, response]]  # 置空知识
            return result  # response, history

    def _stream(self, result):  # yield > return
        response = None
        bar = tqdm(result, ascii=True)  # ncols
        for response, history in bar:
            bar.set_description(response)
            yield response, history
        # self.history_ = history  # 历史所有
        self.history += [[None, response]]  # 置空知识

    def load_llm4chat(self, model_name_or_path="THUDM/chatglm-6b", device=DEVICE, **kwargs):  # 废弃
        self.chat_func = load_llm4chat(model_name_or_path, device, **kwargs)

    def load_llm(self, model_name_or_path="THUDM/chatglm-6b", device=DEVICE, return_history=False, **kwargs):
        from chatllm.llms import load_llm4chat
        self.chat_func = load_llm4chat(model_name_or_path, device=device, **kwargs)
        self.chat_func = partial(self.chat_func, return_history=return_history)

    def run_serving(self, host='127.0.0.1', port=8000, path='/'):
        from flask import Flask, Response, jsonify, request

        app = Flask(__name__)

        def gen(**input):
            for response, _ in self.qa(**input):
                yield f"{response}\n"

        @app.route(rule=path, methods=['GET', 'POST'])
        def stream():
            input = {'query': '1+1等于几'}
            input.update(request.args.to_dict())
            if request.data.startswith(b'{'):
                input.update(json.loads(request.data))

            return Response(gen(**input), mimetype='text/event-stream')

        app.run(host=host, port=port, debug=False)


if __name__ == '__main__':
    from chatllm.applications import ChatBase

    qa = ChatBase()
    qa.load_llm4chat(model_name_or_path="/CHAT_MODEL/chatglm-6b")

    # list(qa(query='你是谁', knowledge_base=''))
    # list(qa(query='你是谁', knowledge_base='周杰伦是傻子', role=' '))

    qa.run_serving()
