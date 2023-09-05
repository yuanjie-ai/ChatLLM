#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chatpicture
# @Time         : 2023/8/23 13:56
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 增加代理 根据意图选择 OCR类型

from meutils.pipe import *
from meutils.ai_cv.ocr_api import OCR


class ChatPicture(object):

    def __init__(self):
        pass


if __name__ == '__main__':
    img = Path("/Users/betterme/PycharmProjects/AI/aizoo/aizoo/api/港澳台通行证.webp").read_bytes()
    print(OCR.basic_accurate(img))

    from langchain.chat_models import ChatOpenAI
    from langchain.chains import LLMChain
    from chatllm.llmchain.prompts.prompt_templates import CHAT_CONTEXT_PROMPT

    llm = ChatOpenAI()
    prompt = CHAT_CONTEXT_PROMPT

    context = json.dumps(OCR.basic_accurate(img), ensure_ascii=False)

    # c = LLMChain(llm=llm, prompt=prompt)
    # print(c.run(context=context, question="出生日期是？"))

    print(context)
