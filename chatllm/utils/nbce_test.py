#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : nbce
# @Time         : 2023/5/30 16:14
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://github.com/bojone/NBCE/blob/main/test.py

from meutils.pipe import *
# ! -*- coding: utf-8 -*-
# Naive Bayes-based Context Extension (NBCE)
# 使用朴素贝叶斯增加LLM的Context处理长度
# 链接：https://kexue.fm/archives/9617
# Torch 2.0 测试通过

import json
import torch
from transformers import AutoTokenizer
from transformers import LlamaForCausalLM
from transformers import TopPLogitsWarper, LogitsProcessorList

# 经过微调的LLAMA
# 下载地址：https://openbuddy.ai/
model_path = '/root/autodl-tmp/7b-trans-chat-0516-bf16'

# 加载tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path)
tokenizer.padding_side = 'left'
tokenizer.pad_token = tokenizer.unk_token

# 加载LLAMA模型
model = LlamaForCausalLM.from_pretrained(model_path, device_map='auto', torch_dtype=torch.bfloat16)
device = torch.device('cuda')

# 加载示例Context
contexts = json.load(open('contexts.json'))

# 示例问题集（一次性问多个问题，NBCE自行根据Context逐一输出答案）
question = """请仔细阅读材料，逐一回答：
- 菲律宾国家电网公司，中国占股多少？
- 领英计划裁员多少人？
- 吉利德收购Pharmasset的价格是多少？
- 丙肝神药Sovaldi在哪一年上市？
- 中亚峰会将在哪里举行？由谁主持？
- 哪个演员由于侮辱人民军队而被立案调查？
- 哪个项目宣称“能过坦克”的水上道路？
- 如果你是默沙东的CEO，你的首要任务是什么？"""

# 拼接context和question
contexts = [''] + contexts  # 添加空Context（无Context预测）
batch = ['User: %s\n\n%s\n\nAssistant:' % (context, question) for context in contexts]
print('Context长度分布：', [len(text) for text in batch])
print('Context总长度：', sum([len(text) for text in batch]))

# Top-P截断
processors = LogitsProcessorList()
processors.append(TopPLogitsWarper(0.95))


@torch.inference_mode()
def generate(max_tokens):
    """Naive Bayes-based Context Extension 演示代码
    """
    inputs = tokenizer(batch, padding='longest', return_tensors='pt').to(device)
    input_ids = inputs.input_ids
    attention_mask = inputs.attention_mask

    print('input_ids', input_ids.shape)
    past_key_values = None
    n = input_ids.shape[0]

    for i in range(max_tokens):
        # 模型输出
        outputs = model(input_ids=input_ids,
                        attention_mask=attention_mask,
                        return_dict=True,
                        use_cache=True,
                        past_key_values=past_key_values
                        )
        past_key_values = outputs.past_key_values

        # ===== 核心代码开始 =====
        beta = 0.25
        logits = outputs.logits[:, -1]
        logits = logits - logits.logsumexp(dim=-1, keepdims=True)
        logits = processors(input_ids, logits)
        k = (logits.exp() * logits.clip(-100, 0)).sum(dim=-1)[1:].argmax() + 1
        logits_max = logits[k]
        logits_uncond = logits[0]
        logits_merged = (1 + beta) * logits_max - beta * logits_uncond
        logits = torch.where(logits_uncond > -100, logits_merged, logits_max)
        # ===== 核心代码结束 =====


        # 构建分布，采样
        # tau = 1是标准的随机采样，tau->0则是贪心搜索
        # 简单起见，这里没有实现topk、topp截断
        tau = 0.01
        probas = torch.nn.functional.softmax(logits[None] / tau, dim=-1)
        next_tokens = torch.multinomial(probas, num_samples=1).squeeze(1)
        if next_tokens[0] == tokenizer.eos_token_id:
            break

        ret = tokenizer.batch_decode(next_tokens)
        print(ret[0], flush=True, end='')

        # prepare for next iteration
        input_ids = next_tokens.unsqueeze(-1).tile(n, 1)
        attention_mask = torch.cat([attention_mask, torch.ones(n, 1, dtype=torch.long, device=device)], dim=-1)


if __name__ == '__main__':
    generate(1000)

"""
========= 输出结果参考 =========

1.菲律宾国家电网公司，中国占股多少？
答：中国国家电网公司持有菲律宾国家电网公司40%的股份。

2.领英计划裁员多少人？
答：领英计划裁员716人。

3.吉利德收购Pharmasset的价格是多少？
答：吉利德收购Pharmasset的价格为110亿美元。

4.丙肝神药Sovaldi在哪一年上市？
答：丙肝神药Sovaldi于2013年上市。

5.中亚峰会将在哪里举行？由谁主持？
答：中亚峰会将在陕西省西安市举行，由国家主席习近平主持。

6.哪个演员由于侮辱人民军队而被立案调查？
答：李昊石因在表演中存在侮辱人民军队的言论而被立案调查。

7.哪个项目宣称“能过坦克”的水上道路？
答：湖北恩施宣称的“能过坦克”水上道路。

8.如果你是默沙东的CEO，你的首要任务是什么？
答：如果我是默沙东的CEO，我的首要任务是如何让基本盘更加坚固，并通过药物联用获得更好的增长。
"""
