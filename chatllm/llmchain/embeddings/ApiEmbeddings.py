#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ApiEmbeddings
# @Time         : 2023/8/10 15:52
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.decorators.retry import retrying

from langchain.embeddings.base import Embeddings


class ApiEmbeddings(BaseModel, Embeddings):
    request_fn: Optional[Callable[[List[str]], List[List[float]]]] = None

    # requests.post('', json={'texts': ['']}).json()['data']

    @retrying
    def _post(self, texts: List[str]) -> List[List[float]]:
        return self.request_fn(texts)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self._post(texts)

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]


if __name__ == '__main__':
    ApiEmbeddings().embed_query('xx')
