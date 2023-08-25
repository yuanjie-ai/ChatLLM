#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : DashScopeEmbeddings
# @Time         : 2023/7/27 13:37
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

import langchain
from langchain.embeddings.dashscope import DashScopeEmbeddings as _DashScopeEmbeddings, embed_with_retry

from meutils.pipe import *
from meutils.np_utils import normalize
from chatllm.llmchain.utils import get_api_key


class DashScopeEmbeddings(_DashScopeEmbeddings):
    chunk_size: int = 25
    """Maximum number of texts to embed in each batch"""
    show_progress_bar: bool = False
    """Whether to show a progress bar when embedding."""
    normalize_embeddings: bool = True
    """多key多线程"""
    get_api_key: Callable[[int], List[str]] = get_api_key

    def embed_documents(
        self, texts: List[str], chunk_size: Optional[int] = 0
    ) -> List[List[float]]:
        n = int(np.ceil(len(texts) / self.chunk_size))
        api_key_set = self.get_api_key(n=n)

        max_workers = np.clip(len(api_key_set), 1, 16).astype(int)  # 最大线程数
        if max_workers > 1:
            embeddings_map = {}
            for i, api_key in enumerate(api_key_set):
                kwargs = self.dict().copy()
                kwargs['dashscope_api_key'] = api_key
                embeddings_map[i] = DashScopeEmbeddings(**kwargs)  # 多个对象实例

            if langchain.debug:
                logger.info([e.dashscope_api_key for e in embeddings_map.values()])
                logger.info(f"Maximum concurrency: {max_workers * self.chunk_size}")

            def __embed_documents(arg):
                idx, texts = arg
                embeddings = embeddings_map.get(idx % max_workers, 0)
                return embeddings._embed_documents(texts)

            return (
                texts | xgroup(self.chunk_size)
                | xenumerate
                | xThreadPoolExecutor(__embed_documents, max_workers)
                | xchain_
            )

        return self._embed_documents(texts)

    def _embed_documents(self, texts: List[str], chunk_size=None) -> List[List[float]]:
        """Call out to DashScope's embedding endpoint for embedding search docs.

        Args:
            texts: The list of texts to embed.
            chunk_size: The chunk size of embeddings. If None, will use the chunk size
                specified by the class.

        Returns:
            List of embeddings, one for each text.
        """

        batched_embeddings = []
        _chunk_size = chunk_size or self.chunk_size

        if self.show_progress_bar:
            _iter = tqdm(range(0, len(texts), _chunk_size))
        else:
            _iter = range(0, len(texts), _chunk_size)

        for i in _iter:
            response = embed_with_retry(
                self,
                input=texts[i: i + _chunk_size],
                text_type="document",
                model=self.model,
                # api_key=api_key
            )
            batched_embeddings += [r["embedding"] for r in response]  # response: embeddings

        return batched_embeddings if not self.normalize_embeddings else normalize(np.array(batched_embeddings)).tolist()

    def embed_query(self, text: str) -> List[float]:
        embedding = super().embed_query(text)
        return embedding if not self.normalize_embeddings else normalize(np.array(embedding)).tolist()

if __name__ == '__main__':
    print(DashScopeEmbeddings().embed_query(text='a'))
