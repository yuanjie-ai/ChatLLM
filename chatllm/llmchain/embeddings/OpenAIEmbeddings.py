#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : OpenAIEmbeddings
# @Time         : 2023/7/11 18:40
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

import langchain
from langchain.embeddings import OpenAIEmbeddings as _OpenAIEmbeddings

from meutils.pipe import *
from chatllm.llmchain.utils import get_api_key


class OpenAIEmbeddings(_OpenAIEmbeddings):
    """多key多线程"""
    get_api_key: Callable[[int], List[str]] = get_api_key
    pre_fn: Optional[Callable[[str], str]] = None

    # class Config:
    #     """Configuration for this pydantic object."""
    #
    #     allow_population_by_field_name = True
    def embed_documents(
        self,
        texts: List[str],
        chunk_size: Optional[int] = 0,
    ) -> List[List[float]]:
        if self.pre_fn: texts = texts | xmap_(self.pre_fn)

        n = int(np.ceil(len(texts) / self.chunk_size))
        api_key_set = self.get_api_key(n=n)

        max_workers = np.clip(len(api_key_set), 1, 32).astype(int)  # 最大线程数
        if max_workers > 1:
            embeddings_map = {}
            for i, api_key in enumerate(api_key_set):
                kwargs = self.dict().copy()
                kwargs.pop('get_api_key', None)  # not permitted
                kwargs['openai_api_key'] = api_key
                embeddings_map[i] = _OpenAIEmbeddings(**kwargs)  # 可以用 OpenAIEmbeddings

            if langchain.debug:
                logger.info([e.openai_api_key for e in embeddings_map.values()])
                logger.info(f"Maximum concurrency: {max_workers * self.chunk_size}")

            def __embed_documents(arg):
                idx, texts = arg
                embeddings = embeddings_map.get(idx % max_workers, 0)
                return embeddings.embed_documents(texts)

            return (
                texts | xgroup(self.chunk_size)
                | xenumerate
                | xThreadPoolExecutor(__embed_documents, max_workers)
                | xchain_
            )

        return super().embed_documents(texts)


if __name__ == '__main__':
    e = OpenAIEmbeddings(chunk_size=5)

    e.get_api_key = partial(get_api_key, n=2)
    # e.openai_api_key = 'xxx'
    print(e.get_api_key())
    print(e.openai_api_key)
    print(e.embed_documents(['x'] * 6))
    print(e.embed_query('x'))
