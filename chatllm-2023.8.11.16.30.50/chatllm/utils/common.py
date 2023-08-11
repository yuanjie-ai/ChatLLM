#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : utils
# @Time         : 2023/4/20 12:50
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

import torch
from transformers import AutoTokenizer, AutoModel

from meutils.pipe import *
from chatllm.utils.gpu_utils import load_chatglm_on_gpus

DEVICE = (
    os.getenv('DEVICE') if 'DEVICE' in os.environ
    else "cuda" if torch.cuda.is_available()
    else "mps" if torch.backends.mps.is_available()
    else "cpu"
)

xgroup = Pipe(lambda ls, step=3, overlap_rate=0: [ls[max(idx - int(step * overlap_rate), 0): idx + step] for idx in
                                                  range(0, len(ls), step)])


def textsplitter(text, chunk_size=512, overlap_rate=0.2, sep=''):  # 简单粗暴
    return text.lower().split() | xjoin(sep) | xgroup(chunk_size, overlap_rate)


def load_llm(model_name_or_path="THUDM/chatglm-6b", device=DEVICE, num_gpus=2, **kwargs):
    model = AutoModel.from_pretrained(model_name_or_path, trust_remote_code=True)
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)

    if torch.cuda.is_available() and device.lower().startswith("cuda"):
        num_gpus = min(num_gpus, torch.cuda.device_count())

        if num_gpus == 1:  # 单卡
            model = model.half().cuda()
            # model.transformer.prefix_encoder.float()
        elif 'chatglm' in model_name_or_path:  # chatglm多卡
            model = load_chatglm_on_gpus(model_name_or_path, num_gpus)
            logger.info('多卡加载模型')

    else:
        model = model.float().to(device)

    return model.eval(), tokenizer


def load_llm4chat(model_name_or_path="THUDM/chatglm-6b", device=DEVICE, num_gpus=2, stream=True, **kwargs):
    model, tokenizer = load_llm(model_name_or_path, device, num_gpus, **kwargs)
    if stream and hasattr(model, 'stream_chat'):
        return partial(model.stream_chat, tokenizer=tokenizer)  # 可以在每一次生成清GPU
    else:
        return partial(model.chat, tokenizer=tokenizer)


if __name__ == '__main__':
    model, tokenizer = load_llm("/CHAT_MODEL/chatglm", device='cpu')
