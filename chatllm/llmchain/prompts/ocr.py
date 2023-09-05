#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ocr
# @Time         : 2023/9/5 16:24
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 通用文本图像智能分析系统

from meutils.pipe import *
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

# context=ocr_result, keys=question # 开票日期,开票人,收款人
ocr_ie_prompt = """
你现在的任务是从OCR文字识别的结果中提取我指定的关键信息。
OCR的文字识别结果使用```符号包围，包含所识别出来的文字，顺序在原始图片中从左至右、从上至下。我指定的关键信息使用[]符号包围。
请注意OCR的文字识别结果可能存在长句子换行被切断、不合理的分词、对应错位等问题，你需要结合上下文语义进行综合判断，以抽取准确的关键信息。
在返回结果时使用json格式，包含一个key-value对，key值为我指定的关键信息，value值为所抽取的结果。
如果认为OCR识别结果中没有关键信息key，则将value赋值为“未找到相关信息”。 请只输出json格式的结果，不要包含其它多余文字！下面正式开始：
OCR文字：```{context}```
要抽取的关键信息：[{question}]。
""".strip()

# {
#     '坐标': [
#         [358.0, 1488.0],
#         [396.0, 1488.0],
#         [396.0, 1554.0],
#         [358.0, 1554.0]
#     ],
#     '文字': '部门'
# }

ocr_qa_prompt = """
你现在的任务是根据OCR文字识别的结果回答问题。
OCR的文字识别结果使用```符号包围，包含所识别出来的文字与文字对应的坐标，顺序在原始图片中从左至右、从上至下。
请注意OCR的文字识别结果可能存在长句子换行被切断、不合理的分词、对应错位等问题，你需要结合上下文语义及坐标进行综合判断，让我们一步一步思考并准确回答问题。
OCR文字识别的结果：```{context}```
问题：{question}
""".strip()
