#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : glm
# @Time         : 2023/7/24 13:47
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://maas.aminer.cn/dev/api#chatglm_pro

from pydantic import root_validator
from langchain.chat_models.openai import ChatOpenAI
from langchain.utils import get_from_dict_or_env

from langchain.adapters.openai import convert_message_to_dict
from langchain.schema.messages import BaseMessage

from meutils.pipe import *
from chatllm.llmchain.completions import ChatGLMCompletion


class ChatGLM(ChatOpenAI):
    """
        chatglm_lite
        chatglm_std
        chatglm_pro
    """
    client: Any  #: :meta private:
    model_name: str = Field(default="chatglm_lite", alias="model")
    openai_api_key: Optional[str] = Field(default=None, alias="chatglm_api_key")

    class Config:
        """Configuration for this pydantic object."""

        allow_population_by_field_name = True

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and python package exists in environment."""
        # 覆盖 openai_api_key
        values["openai_api_key"] = get_from_dict_or_env(
            values, "chatglm_api_key", "CHATGLM_API_KEY"
        )

        values["client"] = ChatGLMCompletion

        if values["n"] < 1:
            raise ValueError("n must be at least 1.")
        if values["n"] > 1 and values["streaming"]:
            raise ValueError("n must be 1 when streaming.")
        return values

    @property
    def _llm_type(self) -> str:
        return Path(__file__).name  # 'ernie'

    def get_num_tokens_from_messages(self, messages: List[BaseMessage]) -> int:
        """Calculate num tokens with tiktoken package.

        Official documentation: https://github.com/openai/openai-cookbook/blob/
        main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb"""
        if sys.version_info[1] <= 7:
            return super().get_num_tokens_from_messages(messages)
        model, encoding = self._get_encoding_model()
        tokens_per_message = 3
        tokens_per_name = 1
        num_tokens = 0
        messages_dict = [convert_message_to_dict(m) for m in messages]
        for message in messages_dict:
            num_tokens += tokens_per_message
            for key, value in message.items():
                # Cast str(value) in case the message value is not a string
                # This occurs with function messages
                num_tokens += len(encoding.encode(str(value)))
                if key == "name":
                    num_tokens += tokens_per_name
        # every reply is primed with <im_start>assistant
        num_tokens += 3
        return num_tokens


if __name__ == '__main__':
    from meutils.pipe import *
    from chatllm.llmchain.llms import ChatGLM

    from langchain.chains import LLMChain
    from langchain.prompts import ChatPromptTemplate

    first_prompt = ChatPromptTemplate.from_template("{q}")

    llm = ChatGLM(streaming=True)
    c = LLMChain(llm=llm, prompt=first_prompt)

    for i in c.run('你是谁'):
        print(i, end='')

    # from chatllm.llmchain.decorators import llm_stream
    # for i in llm_stream(c.run)('你是谁'):
    #     print(i, end='')
