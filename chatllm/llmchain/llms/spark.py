#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : xunfei
# @Time         : 2023/7/24 13:46
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://www.xfyun.cn/doc/spark/Web.html


from pydantic import root_validator
from langchain.chat_models.openai import ChatOpenAI
from langchain.utils import get_from_dict_or_env, get_pydantic_field_names

from meutils.pipe import *
from chatllm.llmchain.completions import SparkBotCompletion


class SparkBot(ChatOpenAI):
    """
    api_key = {APP Id}:{API Key}:{Secret Key}
    """
    client: Any  #: :meta private:
    model_name: str = Field(default="spark-turbo", alias="model")
    openai_api_key: Optional[str] = Field(default=None, alias="spark_api_key")  # ernie_api_key: Optional[str] = None

    class Config:
        """Configuration for this pydantic object."""

        allow_population_by_field_name = True

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and python package exists in environment."""
        # 覆盖 openai_api_key
        values["openai_api_key"] = get_from_dict_or_env(
            values, "spark_api_key", "SPARK_API_KEY"
        )

        values["client"] = SparkBotCompletion

        if values["n"] < 1:
            raise ValueError("n must be at least 1.")
        if values["n"] > 1 and values["streaming"]:
            raise ValueError("n must be 1 when streaming.")
        return values

    @property
    def _llm_type(self) -> str:
        return Path(__file__).name  # 'ernie'


if __name__ == '__main__':
    from meutils.pipe import *
    from chatllm.llmchain.llms import SparkBot

    from langchain.chains import LLMChain
    from langchain.prompts import ChatPromptTemplate
    from langchain.callbacks import get_openai_callback

    first_prompt = ChatPromptTemplate.from_template("{q}")

    llm = SparkBot(streaming=True)
    # with get_openai_callback() as cb:
    #     c = LLMChain(llm=llm, prompt=first_prompt)
    #     print(c.run('你是谁'))
    #
    # print(cb.total_tokens)
    c = LLMChain(llm=llm, prompt=first_prompt)
    for i in c.run('你是谁'):
        print(i, end='')
