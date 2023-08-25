#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : file
# @Time         : 2023/7/15 17:39
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from langchain.text_splitter import *
from langchain.document_loaders import CSVLoader, UnstructuredFileLoader
from langchain.document_loaders.base import Document, BaseLoader
from chatllm.llmchain.document_loaders import TextLoader, Docx2txtLoader, PyMuPDFLoader


class FileLoader(BaseLoader):
    """
        loader = FilesLoader('data/古今医统大全.txt')
        docs = loader.load_and_split()
    """

    def __init__(
        self,
        file_path: Any,
        filename: Optional[str] = None,
        max_workers: int = 3
    ):
        self.file_path = file_path

        self.filename = filename or file_path
        if not isinstance(self.filename, str):
            if hasattr(self.filename, 'name'):
                self.filename = self.filename.name
            else:
                self.filename = str(self.filename)

        self._max_workers = max_workers

    # @staticmethod
    # def _load_one_file(file_args, text_splitter=None):
    #     file_stream, filename = file_args
    #     docs = FileLoader(file_stream, filename).load_and_split(text_splitter)
    #     print(docs)
    #     for idx, doc in enumerate(docs):
    #         doc.metadata['index'] = idx
    #         doc.metadata['source'] = doc.metadata.get('source') or filename
    #     return docs or []
    #
    # @classmethod
    # def load_and_split4multifile(cls, files, text_splitter=None):
    #     _load_one_file = partial(cls._load_one_file, text_splitter=text_splitter)
    #     docs = files | xmap(lambda file: (file.read(), file.name)) | xProcessPoolExecutor(_load_one_file, min(8, len(files))) | xchain_
    #     return docs

    def load_and_split(
        self,
        text_splitter: Optional[TextSplitter] = None,
    ) -> List[Document]:
        """Load Documents and split into chunks. Chunks are returned as Documents.

        Args:
            text_splitter: TextSplitter instance to use for splitting documents.
              Defaults to RecursiveCharacterTextSplitter.

        Returns:
            List of Documents.
        """
        if text_splitter is None:
            separators = ['\n\n', '\r', '\n', '\r\n', '。', '!', '！', '\\?', '？', '……', '…']
            _text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=510,
                chunk_overlap=100,
                add_start_index=True,
                separators=separators
            )
        else:
            _text_splitter = text_splitter
        docs = self.load()
        return _text_splitter.split_documents(docs)

    def load(self) -> List[Document]:

        if self.filename.endswith((".txt",)):
            docs = TextLoader(self.file_path, autodetect_encoding=True).load()

        elif self.filename.endswith((".docx",)):
            docs = Docx2txtLoader(self.file_path).load()

        elif self.filename.endswith((".pdf",)):
            docs = PyMuPDFLoader(self.file_path).load()

        elif self.filename.endswith((".csv",)):
            docs = CSVLoader(self.file_path).load()

        else:
            if isinstance(self.file_path, List) or (
                isinstance(self.file_path, (str, os.PathLike))
                and len(self.file_path) < 256
                and Path(self.file_path).is_file()
            ):
                docs = UnstructuredFileLoader(
                    file_path=self.file_path,
                    strategy="fast",
                ).load()
            else:
                docs = UnstructuredFileLoader(
                    file_path=None,
                    file=self.file_path,
                    file_filename=self.filename,
                    strategy="fast",
                ).load()
                for doc in docs:
                    doc.metadata['source'] = doc.metadata.get('source') or self.filename

        # schema: file_type todo: 增加字段
        # 静态schema怎么设计存储，支持多文档：metadata存文件名字段（可以放多层级）
        # docs[0].metadata['total_length'] = len(docs[0].page_content)
        # docs[0].metadata['file_name'] = Path(docs[0].metadata['source']).name
        # docs[0].metadata['ext'] = {}  # 拓展字段

        return docs


if __name__ == '__main__':
    p = 'text.py'
    # p = '/Users/betterme/PycharmProjects/AI/ChatLLM/data/医/古今医统大全.txt'
    loader = FileLoader(p)
    docs = loader.load_and_split()
    print(docs)
