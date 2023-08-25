#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chatocr
# @Time         : 2023/8/25 16:45
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://aistudio.baidu.com/modelsdetail?modelId=332

from meutils.pipe import *
from IPython.display import Image
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI()

from rapidocr_onnxruntime import RapidOCR

rapid_ocr = RapidOCR()

p = "/Users/betterme/PycharmProjects/AI/MeUtils/meutils/ai_cv/invoice.jpg"
ocr_result, _ = rapid_ocr(p)
Image(p)

key = '识别编号,公司名称,开票日期,开票人,收款人,复核人,金额'

prompt = f"""你现在的任务是从OCR文字识别的结果中提取我指定的关键信息。OCR的文字识别结果使用```符号包围，包含所识别出来的文字，
顺序在原始图片中从左至右、从上至下。我指定的关键信息使用[]符号包围。请注意OCR的文字识别结果可能存在长句子换行被切断、不合理的分词、
对应错位等问题，你需要结合上下文语义进行综合判断，以抽取准确的关键信息。
在返回结果时使用json格式，包含一个key-value对，key值为我指定的关键信息，value值为所抽取的结果。
如果认为OCR识别结果中没有关键信息key，则将value赋值为“未找到相关信息”。 请只输出json格式的结果，不要包含其它多余文字！下面正式开始：
OCR文字：```{ocr_result}```
要抽取的关键信息：[{key}]。"""
print(llm.predict(prompt))
