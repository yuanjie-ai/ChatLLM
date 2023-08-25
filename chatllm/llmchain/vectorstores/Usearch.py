#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : usearch
# @Time         : 2023/8/22 08:49
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 合并【定期】，保存

from meutils.pipe import *
from langchain.vectorstores import USearch as _USearch

from langchain.docstore.document import Document
from langchain.docstore.in_memory import InMemoryDocstore
from langchain.embeddings.base import Embeddings


class USearch(_USearch):

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        threshold: float = 0.5,
        **kwargs: Any,
    ) -> List[Document]:

        docs_and_scores = self.similarity_search_with_score(query, k)

        docs = []
        for doc, score in docs_and_scores:
            score = round(1 - score, 2)
            if score > threshold:
                doc.metadata['score'] = score
                docs.append(doc)
        return docs

    @classmethod
    def from_texts(
        cls,
        texts: List[str],
        embedding: Embeddings,
        metadatas: Optional[List[Dict]] = None,
        ids: Optional[np.ndarray] = None,
        metric: str = "cos",
        **index_kwargs: Any,  # from_documents kwargs
    ) -> _USearch:
        """Construct USearch wrapper from raw documents.
        This is a user friendly interface that:
            1. Embeds documents.
            2. Creates an in memory docstore
            3. Initializes the USearch database
        This is intended to be a quick way to get started.

        Example:
            .. code-block:: python

                from langchain.vectorstores import USearch
                from langchain.embeddings import OpenAIEmbeddings

                embeddings = OpenAIEmbeddings()
                usearch = USearch.from_texts(texts, embeddings)
        """
        embeddings = embedding.embed_documents(texts)

        documents: List[Document] = []
        if ids is None:
            ids = list(map(str, range(len(texts))))
        for i, text in enumerate(texts):
            metadata = metadatas[i] if metadatas else {}
            documents.append(Document(page_content=text, metadata=metadata))

        docstore = InMemoryDocstore(dict(zip(ids, documents)))

        from usearch.index import Index
        index = Index(ndim=len(embeddings[0]), metric=metric, **index_kwargs)
        index.add(np.array(ids), np.array(embeddings))

        return cls(embedding, index, docstore, ids)

    def save_local(self, folder_path: str, index_name: str = "index") -> None:
        """ save index and docstore

        :param folder_path:
        :param index_name:
        :return:
        """

        path = Path(folder_path)
        path.mkdir(exist_ok=True, parents=True)

        self.index.save(path / f"{index_name}.usearch")
        pkl_dump(self.docstore, path / f"{index_name}.pkl")  # 保存 InMemoryDocstore(dict(zip(ids, documents)))

    @classmethod
    def load_local(
        cls,
        folder_path: str,
        embeddings: Embeddings,
        index_name: str = "index",
        **kwargs: Any,
    ) -> _USearch:

        path = Path(folder_path)

        from usearch.index import Index
        index = Index.restore(str(path / f"{index_name}.usearch"))  # os.PathLike对象读取为空
        docstore: InMemoryDocstore = pkl_load(path / f"{index_name}.pkl")

        return cls(embeddings, index, docstore, ids=list(docstore._dict))

    def merge_from(self, target: _USearch) -> None:
        """从0开始建索引"""

        vectors = np.r_[self.index.vectors, target.index.vectors]
        ids = list(map(str, range(len(vectors))))

        self.index.clear()  # 清空重建
        self.index.add(ids, vectors)  # search字符串可能报错

        documents = list(self.docstore._dict.values()) + list(target.docstore._dict.values())

        self.docstore = InMemoryDocstore(dict(zip(ids, documents)))


if __name__ == '__main__':
    from chatllm.llmchain.vectorstores import USearch
    from chatllm.llmchain.embeddings import HuggingFaceEmbeddings

    model_name = '/Users/betterme/PycharmProjects/AI/m3e-small'
    encode_kwargs = {'normalize_embeddings': True, 'show_progress_bar': True, 'device': 'mps'}
    embeddings = HuggingFaceEmbeddings(model_name=model_name, encode_kwargs=encode_kwargs)

    ann = USearch.from_texts(['1', '2', '3'], embeddings, dtype='i8')

    print(ann.similarity_search('1'))
