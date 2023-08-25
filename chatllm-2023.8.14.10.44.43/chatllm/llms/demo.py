#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : __init__.py
# @Time         : 2023/5/19 17:34
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *

import torch
from transformers import AutoTokenizer, AutoModel, LlamaForCausalLM


class LLM(object):

    def __init__(self, model_name_or_path="THUDM/chatglm-6b", device='cpu', max_num_gpus=2):
        self.model_name_or_path = model_name_or_path
        self.device = device
        self.max_num_gpus = max_num_gpus

        self.model, self.tokenizer = self.load()

    def load(self):
        tokenizer = AutoTokenizer.from_pretrained(self.model_name_or_path, trust_remote_code=True)

        if 'llama' in self.model_name_or_path.lower():  # llama 系列
            model = LlamaForCausalLM.from_pretrained(self.model_name_or_path, trust_remote_code=True)
        else:
            model = AutoModel.from_pretrained(self.model_name_or_path, trust_remote_code=True)

        if torch.cuda.is_available() and self.device.lower().startswith("cuda"):
            num_gpus = min(self.max_num_gpus, torch.cuda.device_count())

            if num_gpus == 1:  # 单卡
                model = model.half().cuda()
            else:
                pass  # todo: 多卡
        else:
            model = model.float().to(self.device)

        return model.eval(), tokenizer

    def chat(self):
        return partial(self.model.stream_chat, tokenizer=self.tokenizer)  # 思考 统一模式
