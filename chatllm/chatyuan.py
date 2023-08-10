#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chatyuan
# @Time         : 2023/4/27 16:42
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
# 加载模型
from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained("ClueAI/ChatYuan-large-v2")
model = T5ForConditionalGeneration.from_pretrained("ClueAI/ChatYuan-large-v2")


def preprocess(text):
    text = text.replace("\n", "\\n").replace("\t", "\\t")
    return text


def postprocess(text):
    return text.replace("\\n", "\n").replace("\\t", "\t").replace('%20', '  ')


def answer(query, knowledge_base='', role='', do_sample=True, top_p=0.9, temperature=0.7):
    text = """{role}
            用户：
            基于以下已知信息，简洁和专业的来回答问题。
            如果无法从中得到答案，请说 "根据已知信息无法回答该问题" 或 "没有提供足够的信息"，不允许在答案中添加编造成分，答案请使用中文。
            已知信息: {context}
            问题：{question}
            小元：
            """.strip().format(role=role or os.environ.get('LLM_ROLE', ''), context=knowledge_base or '请自由回答',
                               question=query)

    text = text.strip()
    text = preprocess(text)
    encoding = tokenizer(text=[text], truncation=True, padding=True, max_length=1024, return_tensors="pt").to(
        model.device)
    out = model.generate(**encoding, return_dict_in_generate=True, output_scores=False, max_new_tokens=1024,
                         do_sample=do_sample, top_p=top_p, temperature=temperature, no_repeat_ngram_size=12)
    out_text = tokenizer.batch_decode(out["sequences"], skip_special_tokens=True)
    return postprocess(out_text[0])


if __name__ == '__main__':
    query = '你是谁'
    print(answer(query))
