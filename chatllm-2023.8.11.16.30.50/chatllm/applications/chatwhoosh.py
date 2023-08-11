#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chatwhoosh
# @Time         : 2023/4/26 19:04
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.hash_utils import md5
from meutils.easy_search.es import EasySearch

from chatllm.applications import ChatBase

from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer


class ChatWhoosh(ChatBase, EasySearch):

    def __init__(self, indexdir='whoosh_index', indexname='MAIN', **kwargs):
        ChatBase.__init__(self, **kwargs)
        EasySearch.__init__(self, indexdir, indexname)
        self.recall = pd.DataFrame({'id': [], 'text': [], 'score': []})

    def qa(self, query, topk=3, threshold=0.66, **kwargs):
        df = self.find(query, topk, threshold)
        if len(df) == 0:
            logger.warning('召回内容为空!!!')
        knowledge_base = '\n'.join(df.text)

        return self._qa(query, knowledge_base, **kwargs)

    def find(self, query, topk=3, threshold=0.66, **kwargs):
        df = super().find(defaultfield='text', querystring=query, limit=topk, **kwargs)
        if len(df):
            self.recall = df.query(f'score > {threshold}')
        return self.recall

    def create_index(self, texts, id_mapping=md5, **kwargs):
        ids = map(id_mapping, texts)
        df = pd.DataFrame({'id': ids, 'text': texts})
        schema = Schema(
            id=ID(stored=True),
            text=TEXT(stored=True, analyzer=ChineseAnalyzer(cachesize=-1))  # 无界缓存加速
        )
        super().create_index(df, schema, **kwargs)


if __name__ == '__main__':
    from chatllm.applications.chatwhoosh import ChatWhoosh

    cw = ChatWhoosh(indexdir='whoosh_index')
    cw.create_index(texts=['周杰伦'] * 10)
    print(cw.find('周杰伦'))
