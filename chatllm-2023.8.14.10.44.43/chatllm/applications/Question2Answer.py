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
from meutils.docarray_ import DocumentArray
from meutils.decorators import clear_cuda_cache
from meutils.request_utils.crawler import Crawler


class Question2Answer(object):

    def __init__(self, chat_func, prompt_template=None):
        self.chat_func = chat_func
        # self.query_embedd = lru_cache()(query_embedd)  # 缓存
        # self.docs = docs

        self.history = []

        self.prompt_template = prompt_template
        if prompt_template is None:
            self.prompt_template = self.default_document_prompt

    @abstractmethod
    def qa(self):
        raise NotImplementedError("overwrite method!!!")

    def search4qa(self):
        pass

    def crawler4qa(self, query,
                   url="https://top.baidu.com/board?tab=realtime",
                   xpath='//*[@id="sanRoot"]/main/div[2]/div/div[2]/div[*]/div[2]/a/div[1]//text()', **kwargs):
        knowledge_base = Crawler(url).xpath(xpath)

        return self._qa(query, knowledge_base, **kwargs)

    def ann4qa(self, query, query_embedd=None, da: DocumentArray = None, topk=3, **kwargs):

        # ann召回知识
        v = query_embedd(query)
        knowledge_base = da.find(v, topk=topk)[0].texts  # [:, ('text', 'scores__cosine__value')]

        return self._qa(query, knowledge_base, **kwargs)

    @clear_cuda_cache
    def _qa(self, query, knowledge_base='', max_turns=1, print_knowledge_base=False):
        if knowledge_base:
            query = self.prompt_template.format(context=knowledge_base, question=query)

            if print_knowledge_base:
                pprint({'knowledge_base': knowledge_base})

        result = self.chat_func(query=query, history=self.history[-max_turns:])

        if isinstance(result, types.GeneratorType):
            return self._stream(result)
        else:  # list(self._stream(result)) 想办法合并
            response, history = result
            # self.history_ = history  # 历史所有
            self.history += [[None, response]]  # 置空知识

        return response

    def _stream(self, result):  # yield > return
        response = None
        for response, history in tqdm(result, desc='Stream'):
            yield response, history
        # self.history_ = history  # 历史所有
        self.history += [[None, response]]  # 置空知识

    @property
    def default_document_prompt(self):
        prompt_template = """
            基于以下已知信息，简洁和专业的来回答用户的问题。
            如果无法从中得到答案，请说 "根据已知信息无法回答该问题" 或 "没有提供足够的相关信息"，不允许在答案中添加编造成分，答案请使用中文。
            已知内容:
            {context}
            问题:
            {question}
            """.strip()

        return prompt_template


if __name__ == '__main__':
    from chatllm.utils import llm_load

    model, tokenizer = llm_load("/Users/betterme/PycharmProjects/AI/CHAT_MODEL/chatglm")
    qa = Question2Answer(
        # chat_func=partial(model.stream_chat, tokenizer=tokenizer),
        chat_func=partial(model.chat, tokenizer=tokenizer),

    )

    # for i, _ in qa._qa('1+1'):
    #     print(i, flush=True)
    print(qa._qa('1+1'))
