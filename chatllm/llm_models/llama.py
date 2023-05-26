#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : llama_ziya
# @Time         : 2023/5/19 17:56
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from chatllm.utils import DEVICE

from transformers import AutoTokenizer
from transformers import LlamaForCausalLM
import torch

# device = torch.device("cuda")
#
# query = "帮我写一份去西安的旅游计划"
# model = LlamaForCausalLM.from_pretrained('IDEA-CCNL/Ziya-LLaMA-13B-v1', torch_dtype=torch.float16, device_map="auto")
# tokenizer = AutoTokenizer.from_pretrained('IDEA-CCNL/Ziya-LLaMA-13B-v1')
# inputs = '<human>:' + query.strip() + '\n<bot>:'
#
# input_ids = tokenizer(inputs, return_tensors="pt").input_ids.to(device)
# generate_ids = model.generate(
#     input_ids,
#     max_new_tokens=1024,
#     do_sample=True,
#     top_p=0.85,
#     temperature=1.0,
#     repetition_penalty=1.,
#     eos_token_id=2,
#     bos_token_id=1,
#     pad_token_id=0)
# output = tokenizer.batch_decode(generate_ids)[0]
# print(output)


@torch.no_grad()
def chat(tokenizer, query: str, history: List[Tuple[str, str]] = None, max_length: int = 2048, num_beams=1,
         do_sample=True, top_p=0.7, temperature=0.95, **kwargs):
    history = history or []

    gen_kwargs = {
        "max_new_tokens": max_length,
        "do_sample": do_sample,
        "top_p": top_p,
        "temperature": temperature,
        "num_beams": num_beams,
        **kwargs
    }
    if not history:
        prompt = query
    else:
        prompt = ""
        for i, (old_query, response) in enumerate(history):
            prompt += f"[Round {i}]\n<human>:{old_query}\n<bot>:{response}\n"
        prompt += f"[Round {len(history)}]\n<human>:{query}\n<bot>:"

    input_ids = tokenizer([prompt], return_tensors="pt", padding=True).to(model.device)
    generate_ids = model.generate(**input_ids, **gen_kwargs)

    response = tokenizer.batch_decode(generate_ids)[0]
    history += [(query, response)]
    return response, history
