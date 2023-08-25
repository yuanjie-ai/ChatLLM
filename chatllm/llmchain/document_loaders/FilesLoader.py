#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : file
# @Time         : 2023/7/15 17:39
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo: 文件流

from meutils.pipe import *
from langchain.text_splitter import *
from langchain.document_loaders import *
from langchain.document_loaders.base import Document, BaseLoader
from chatllm.llmchain.document_loaders import TextLoader, Docx2txtLoader, PyMuPDFLoader


class FilesLoader(BaseLoader):
    """
        loader = FilesLoader('data/古今医统大全.txt')
        docs = loader.load_and_split()
    """

    def __init__(self, file_paths: Union[str, list], max_workers=3):
        self.file_paths = [file_paths] if isinstance(file_paths, str) else file_paths
        self._max_workers = max_workers

    def load(self) -> List[Document]:
        return self.file_paths | xmap(str) | xProcessPoolExecutor(self._load_file, self._max_workers) | xchain_

    @staticmethod
    def _load_file(filepath) -> List[Document]:  # 重写
        file = str(filepath).lower()
        if file.endswith((".txt",)):
            docs = TextLoader(filepath, autodetect_encoding=True).load()

        elif file.endswith((".docx",)):
            docs = Docx2txtLoader(filepath).load()

        elif file.endswith((".pdf",)):
            docs = PyMuPDFLoader(filepath).load()
            doc = Document(page_content='', metadata={'source': filepath})
            for _doc in docs:
                doc.page_content += _doc.page_content.strip()
            docs = [doc]

        elif file.endswith((".csv",)):
            docs = CSVLoader(filepath).load()

        else:
            docs = UnstructuredFileLoader(filepath, mode='single', strategy="fast").load()  # todo： 临时文件

        # schema: file_type todo: 增加字段
        # 静态schema怎么设计存储，支持多文档：metadata存文件名字段（可以放多层级）
        docs[0].metadata['total_length'] = len(docs[0].page_content)
        docs[0].metadata['file_name'] = Path(docs[0].metadata['source']).name
        docs[0].metadata['ext'] = {}  # 拓展字段

        return docs

    def lazy_load(self) -> Iterator[Document]:
        pass


if __name__ == '__main__':
    loader = FilesLoader('data/古今医统大全.txt')
    docs = loader.load_and_split()
    print(docs)
