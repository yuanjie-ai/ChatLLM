#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : pdf
# @Time         : 2023/6/30 18:58
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from langchain.document_loaders.parsers.pdf import BaseBlobParser, Blob, Document
from langchain.document_loaders.pdf import PyMuPDFLoader as _PyMuPDFLoader

from meutils.pipe import *
from meutils.fileparser import stream_parser


class PyMuPDFLoader(_PyMuPDFLoader):
    """Loader that uses PyMuPDF to load PDF files."""

    def __init__(self, file_path: Any) -> None:
        """Initialize with a file path."""
        try:
            import fitz  # noqa:F401
        except ImportError:
            raise ImportError(
                "`PyMuPDF` package not found, please install it with "
                "`pip install pymupdf`"
            )

        self.file_path = file_path

    def load(self, **kwargs: Optional[Any]) -> List[Document]:
        if (
            isinstance(self.file_path, (str, os.PathLike))
            and len(self.file_path) < 256
            and Path(self.file_path).is_file()
        ):
            return _PyMuPDFLoader(self.file_path).load()  # 按页

        filename, file_stream = stream_parser(self.file_path)
        text, metadata = self.get_text(file_stream)
        return [Document(page_content=text, metadata=metadata)]

    @staticmethod
    def get_text(stream):
        import fitz
        doc = fitz.Document(stream=stream)
        return '\n'.join(page.get_text().strip() for page in doc), {'total_pages': len(doc), **doc.metadata}


if __name__ == '__main__':
    f = open('/Users/betterme/PycharmProjects/AI/ChatLLM/data/中职职教高考政策解读.pdf')
    print(PyMuPDFLoader(f).load())
