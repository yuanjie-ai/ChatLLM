#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ann4qa
# @Time         : 2023/4/24 18:10
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :


from meutils.pipe import *
from meutils.np_utils import cosine_topk
from chatllm.applications import ChatBase

from sentence_transformers import SentenceTransformer


class ChatANN(ChatBase):

    def __init__(self, backend='in_memory', encode_model="moka-ai/m3e-small", **kwargs):
        """
        :param backend:
            'in_memory' # todo: 支持更多后端
        :param encode_model:
            "nghuyong/ernie-3.0-nano-zh"
            "shibing624/text2vec-base-chinese"
            "GanymedeNil/text2vec-large-chinese"
        :param kwargs:
        """
        super().__init__(**kwargs)
        self.backend = backend
        self.encode = SentenceTransformer(encode_model).encode  # 加缓存，可重新set

        # create index
        self.index = None

        # 召回结果df
        self.recall = pd.DataFrame({'id': [], 'text': [], 'score': []})

    def qa(self, query, topk=3, threshold=0.66, **kwargs):
        df = self.find(query, topk, threshold)
        if len(df):
            knowledge_base = '\n'.join(df.text)
            return self._qa(query, knowledge_base, **kwargs)
        logger.error('召回内容为空!!!')

    def find(self, query, topk=5, threshold=0.66):  # 返回df
        v = self.encode([query])  # ndim=2

        if self.backend == 'in_memory':
            idxs, scores = cosine_topk(v, np.array(self.index.embedding.tolist()), topk)

            self.recall = (
                self.index.iloc[idxs, :]
                .assign(score=scores)
                .query(f'score > {threshold}')
            )

        return self.recall

    def create_index(self, texts):  # todo：增加 encode_model参数
        embeddings = self.encode(texts, show_progress_bar=True)
        if self.backend == 'in_memory':
            self.index = pd.DataFrame({'text': texts, 'embedding': embeddings.tolist()})

        return self.index


if __name__ == '__main__':

    qa = ChatANN(encode_model="nghuyong/ernie-3.0-nano-zh")
    qa.load_llm(model_name_or_path="/CHAT_MODEL/chatglm-6b")
    qa.create_index(['周杰伦'] * 10)

    for i in qa(query='有几个周杰伦'):
        print(i, end='')
    print(qa.recall)
