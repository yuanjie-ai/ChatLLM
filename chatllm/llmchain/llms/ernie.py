#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ernie
# @Time         : 2023/7/31 13:04
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from pydantic import root_validator
from langchain.chat_models.openai import ChatOpenAI
from langchain.utils import get_from_dict_or_env

from langchain.adapters.openai import convert_message_to_dict
from langchain.schema.messages import BaseMessage

from meutils.pipe import *
from chatllm.llmchain.completions import ErnieBotCompletion


class ErnieBot(ChatOpenAI):
    """
    ernie_api_key = {API Key}:{Secret Key}

    "ernie-bot"
    "ernie-bot-turbo-0725"
    """
    client: Any  #: :meta private:
    model_name: str = Field(default="ernie-bot", alias="model")  # eb-instant，
    openai_api_key: Optional[str] = Field(default=None, alias="ernie_api_key")  # ernie_api_key: Optional[str] = None

    class Config:
        """Configuration for this pydantic object."""

        allow_population_by_field_name = True

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and python package exists in environment."""
        # 覆盖 openai_api_key
        values["openai_api_key"] = get_from_dict_or_env(
            values, "ernie_api_key", "ERNIE_API_KEY"
        )

        values["client"] = ErnieBotCompletion

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
    from chatllm.llmchain.llms import ErnieBot

    from langchain.chains import LLMChain
    from langchain.prompts import ChatPromptTemplate

    prompt = ChatPromptTemplate.from_template("{q}")

    llm = ErnieBot()
    # c = LLMChain(llm=llm, prompt=prompt)
    # print(c.run('你是谁'))

    prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

    {context}

    Question: {question}
    Helpful Answer:"""
    prompt = ChatPromptTemplate.from_template(prompt_template)

    c = LLMChain(llm=llm, prompt=prompt)
    # print(c.run(question='灭霸是谁', context='灭霸是周杰伦'))

    # 计算token
    m = prompt.format_messages(question='灭霸是谁', context='灭霸是周杰伦')
    # m = prompt.format_prompt(question='灭霸是谁', context='灭霸是周杰伦').to_messages()

    print(llm.get_num_tokens_from_messages(m))
