#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ChatPDF
# @Time         : 2023/4/21 11:44
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.office_automation.pdf import extract_text, pdf2text

from chatllm.utils import textsplitter
from chatllm.applications.chatann import ChatANN


class ChatPDF(ChatANN):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_index(self, file_or_text, textsplitter=textsplitter):  # todo 多篇 增加 parser loader

        texts = extract_text(file_or_text)
        texts = textsplitter(texts)
        return super().create_index(texts)


if __name__ == '__main__':
    # filename = '../../data/财报.pdf'
    # bytes_array = Path(filename).read_bytes()
    # texts = extract_text(bytes_array)
    # texts = textsplitter(texts)
    # print(texts)
    from chatllm.applications.chatpdf import ChatPDF

    qa = ChatPDF(encode_model='nghuyong/ernie-3.0-nano-zh')  # 自动建索引
    qa.load_llm(model_name_or_path='/CHAT_MODEL/chatglm-6b', device='cpu')
    qa.create_index('../../data/财报.pdf')

    for i in qa(query='东北证券主营业务', topk=1, threshold=0.8):
        print(i, end='')

    # 召回结果
    print(qa.recall)
