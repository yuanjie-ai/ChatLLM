#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chatocr
# @Time         : 2023/8/25 16:45
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 基于LLM+OCR技术的通用文本图像智能分析系统 https://aistudio.baidu.com/modelsdetail?modelId=332
# https://www.modelscope.cn/studios/liekkas/RapidOCRDemo/files
# https://mp.weixin.qq.com/s/Q9ubSQHhEgpn2Yf6ndoi5w

from meutils.pipe import *
from chatllm.llmchain.applications import ChatBase
from chatllm.llmchain.prompts.ocr import ocr_ie_prompt, ocr_qa_prompt
from chatllm.llmchain.document_loaders import UnstructuredImageLoader


class ChatOCR(ChatBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def chat(self, prompt, file_path=None, prompt_template=ocr_ie_prompt):
        prompt = prompt_template.format(context=self.context(file_path), question=prompt)
        return super().chat(prompt)

    @lru_cache()
    def context(self, file_path):  # todo: 增加 baidu api & qa 问答
        docs = UnstructuredImageLoader(file_path, strategy='ocr_only').load()
        return docs[0].page_content

    def display(self, file_path, width=600):
        from IPython.display import Image
        return Image(file_path, width=width)


if __name__ == '__main__':
    from meutils.pipe import *
    from chatllm.llmchain.applications import ChatOCR

    llm = ChatOCR()
    # file_path = "/Users/betterme/PycharmProjects/AI/MeUtils/meutils/ai_cv/invoice.jpg"
    #
    # llm.chat('识别编号,公司名称,开票日期,开票人,收款人,复核人,金额', file_path=file_path) | xprint
    # print(llm.display(file_path, 700))

    file_path = "/Users/betterme/PycharmProjects/AI/MeUtils/meutils/ai_cv/2.jpg"
    for i in llm.chat('交易编码', file_path=file_path):
        print(i, end='')
    print(llm.display(file_path, 700))



