#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chatglm
# @Time         : 2023/5/19 17:55
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

import torch
from transformers import AutoTokenizer, AutoModel

# ME
from meutils.pipe import *
from chatllm.utils.gpu_utils import load_chatglm_on_gpus


def load_llm(model_name_or_path="THUDM/chatglm-6b", device='cpu', num_gpus=2):
    model = AutoModel.from_pretrained(model_name_or_path, trust_remote_code=True)
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)

    if torch.cuda.is_available() and device.lower().startswith("cuda"):
        print(os.popen("nvidia-smi").read())
        num_gpus = min(num_gpus, torch.cuda.device_count())

        if num_gpus == 1:  # 单卡
            model = model.half().cuda()
            # model.transformer.prefix_encoder.float()
        elif 'chatglm' in model_name_or_path:  # chatglm多卡
            model = load_chatglm_on_gpus(model_name_or_path, num_gpus)

    else:
        model = model.float().to(device)

    return model.eval(), tokenizer


def load_llm4chat(model_name_or_path="THUDM/chatglm-6b", device='cpu', num_gpus=2, **kwargs):
    model, tokenizer = load_llm(model_name_or_path, device, num_gpus)

    def stream_chat(query, history=None, return_history=False, **chat_kwargs):  # 是否增加全量更新 full_update=False,
        """
        for i in chat('1+1', return_history=False):
            print(i, end='')
        """
        # chat_kwargs 标准化: max_tokens, temperature, top_p
        chat_kwargs = {**kwargs, **chat_kwargs}
        chat_kwargs['max_length'] = int(chat_kwargs.get('max_tokens') or 1024 * 8)

        idx = 0
        for response, history in model.stream_chat(tokenizer=tokenizer, query=query, history=history, **chat_kwargs):
            ret = response[idx:]
            if ret[-1:] == "\uFFFD":
                continue

            idx = len(response)
            if return_history:
                yield ret, history
            else:
                yield ret

    return stream_chat


if __name__ == '__main__':
    for i in load_llm4chat('/CHAT_MODEL/chatglm-6b')('你好', return_history=False):
        print(i, end='')
