#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : __init__
# @Time         : 2023/5/26 13:29
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *


def load_llm4chat(model_name_or_path="THUDM/chatglm-6b", device='cpu', num_gpus=2, model_base=None, **kwargs):
    if not model_base:  # 模型基座
        model_base = Path(model_name_or_path).name.lower()
        for p in Path(__file__).parent.glob('*.py'):
            if p.stem in model_base:
                # logger.warning(p) # 自动推断模型基座
                model_base = p.stem

    model_base = importlib.import_module(f"chatllm.llms.{model_base}")
    return model_base.load_llm4chat(
        model_name_or_path=model_name_or_path,
        device=device,
        num_gpus=num_gpus,
        **kwargs)


if __name__ == '__main__':
    # print(load_llm4chat('/Users/betterme/PycharmProjects/AI/CHAT_MODEL/chatglm-6b'))
    print(Path(__file__).parent)
