#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2023/7/4 08:56
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from langchain import LLMChain, OpenAI, PromptTemplate
from langchain.document_loaders.base import Document

from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.chains.base import Chain

# prompt_template = "Tell me a {adjective} joke"
# prompt = PromptTemplate(
#     input_variables=["adjective"], template=prompt_template
# )

template2prompt = PromptTemplate.from_template


def docs2dataframe(docs: List[Document]) -> pd.DataFrame:
    return pd.DataFrame(map(lambda doc: {**doc.metadata, **{'page_content': doc.page_content}}, docs))


def dataframe2docs(df: pd.DataFrame) -> List[Document]:
    df = df.copy()
    docs = []
    for page_content, metadata in zip(df.pop('page_content'), df.to_dict(orient='records')):
        docs.append(Document(page_content=page_content, metadata=metadata))
    return docs


# def get_api_key(n: int = 1, env_name='OPENAI_API_KEY_SET') -> List[str]:
#     """
#
#     :param n:
#     :param env_name:
#     :return:
#     """
#     """获取keys"""
#     openai_api_key_set = (
#         os.getenv(env_name, "").replace(' ', '').strip(',').strip().split(',') | xfilter | xset
#     )
#     openai_api_key_path = os.getenv("OPENAI_API_KEY_PATH", '')
#     if Path(openai_api_key_path).is_file():
#         openai_api_key_set = set(Path(openai_api_key_path).read_text().strip().split())
#     return list(openai_api_key_set)[:n]


def get_api_key(n: int = 1, env_name='OPENAI_API_KEY') -> List[str]:
    """

    :param n:
    :param env_name:
        OPENAI_API_KEY
        DASHSCOPE_API_KEY
    :return:
    """
    _ = os.getenv(env_name)
    if _:
        return [_]

    return []


if __name__ == '__main__':
    print(get_api_key(env_name='xxsas'))
