#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : docx
# @Time         : 2023/8/15 17:08
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from langchain.text_splitter import *
from langchain.document_loaders import Docx2txtLoader as _Docx2txtLoader
from langchain.document_loaders.base import Document, BaseLoader

from meutils.pipe import *
from meutils.fileparser import stream_parser


class Docx2txtLoader(_Docx2txtLoader):
    def __init__(self, file_path: Any) -> None:
        """Initialize with a file path."""
        try:
            import docx2txt  # noqa:F401
        except ImportError:
            raise ImportError(
                "`PyMuPDF` package not found, please install it with "
                "`pip install docx2txt`"
            )

        self.file_path = file_path

    def load(self) -> List[Document]:

        if (
            isinstance(self.file_path, (str, os.PathLike))
            and len(self.file_path) < 256
            and Path(self.file_path).is_file()
        ):
            return _Docx2txtLoader(self.file_path).load()

        import docx2txt

        filename, file_stream = stream_parser(self.file_path)
        return [
            Document(
                page_content=docx2txt.process(io.BytesIO(file_stream)),
                metadata={"source": filename},
            )
        ]


if __name__ == '__main__':
    p = '/Users/betterme/PycharmProjects/AI/ChatLLM/data/吉林碳谷报价材料.docx'
    print(Docx2txtLoader(p).load())
    print(Docx2txtLoader(open(p)).load())
    print(Docx2txtLoader(open(p, 'rb')).load())
    print(Docx2txtLoader(open(p, 'rb').read()).load())
