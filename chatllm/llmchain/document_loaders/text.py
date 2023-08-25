#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : TextLoader
# @Time         : 2023/8/15 15:05
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from langchain.text_splitter import *
from langchain.document_loaders import TextLoader as _TextLoader
from langchain.document_loaders.base import Document, BaseLoader

from meutils.pipe import *
from meutils.fileparser import stream_parser


class TextLoader(_TextLoader):
    def __init__(
        self,
        # Union[str, bytes, bytearray, os.PathLike, io.BytesIO, io.TextIOBase, io.BufferedReader]
        file_path: Any,
        encoding: Optional[str] = None,
        autodetect_encoding: bool = False,
    ):
        """Initialize with file path."""
        self.file_path = file_path
        self.encoding = encoding
        self.autodetect_encoding = autodetect_encoding

    def load(self) -> List[Document]:
        if (
            isinstance(self.file_path, (str, os.PathLike))
            and len(self.file_path) < 256
            and Path(self.file_path).is_file()
        ):
            return _TextLoader(self.file_path, autodetect_encoding=True).load()

        filename, file_stream = stream_parser(self.file_path)
        if isinstance(file_stream, (bytes, bytearray)):
            file_stream = file_stream.decode()

        return [Document(page_content=file_stream, metadata={"source": filename})]


if __name__ == '__main__':
    print(TextLoader('pdf.py').load())
    print(TextLoader(open('pdf.py')).load())
    print(TextLoader(open('pdf.py').read()).load())
    print(TextLoader(open('pdf.py', 'rb')).load())
    print(TextLoader(open('pdf.py', 'rb').read()).load())
