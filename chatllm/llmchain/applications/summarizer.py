#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : summarize
# @Time         : 2023/8/9 14:44
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from langchain.text_splitter import *
from langchain.schema.language_model import BaseLanguageModel
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain

# ME
from meutils.pipe import *
from chatllm.llmchain.decorators import llm_stream
from chatllm.llmchain.document_loaders import FilesLoader
from chatllm.llmchain.prompts.prompt_templates import summary_prompt_template, question_generation_prompt_template


class Summarizer(object):

    def __init__(self, llm: Optional[BaseLanguageModel] = None):
        self.llm = llm or ChatOpenAI(model="gpt-3.5-turbo-16k-0613", temperature=0, streaming=True)

    @logger.catch
    def generate(self, docs: List[Document], max_tokens: int = 10000, prompt_template: str = summary_prompt_template):
        chain_type = 'stuff'
        if sum((len(doc.page_content) for doc in docs)) > max_tokens:
            chain_type = 'map_reduce'

        logger.debug(chain_type)

        self.chain = load_summarize_chain(
            self.llm,
            chain_type=chain_type,
            prompt=ChatPromptTemplate.from_template(prompt_template)
        )
        return self.chain.run(docs)

    @staticmethod
    def load_file(
        file_paths,
        max_workers=3,
        chunk_size=2000,
        chunk_overlap=200,
        separators: Optional[List[str]] = None
    ) -> List[Document]:
        """支持多文件"""
        loader = FilesLoader(file_paths, max_workers=max_workers)
        separators = separators or ['\n\n', '\r', '\n', '\r\n', '。', '!', '！', '\\?', '？', '……', '…']
        textsplitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            add_start_index=True,
            separators=separators
        )
        docs = loader.load_and_split(textsplitter)
        return docs


if __name__ == '__main__':
    s = Summarizer()

    docs = s.load_file('/Users/betterme/PycharmProjects/AI/ChatLLM/data/姚明.txt')

    # print(s.generate(docs))
    # print(s.generate(docs, prompt_template=question_generation_prompt_template))

    chain = load_summarize_chain(
        s.llm,
        prompt=ChatPromptTemplate.from_template(summary_prompt_template)
    )
    # print(chain.run(docs))
    # print(chain.run({'input_documents': docs, "question": None}))
    print(chain.run({'input_documents': docs, "question": '你是谁？'}))

