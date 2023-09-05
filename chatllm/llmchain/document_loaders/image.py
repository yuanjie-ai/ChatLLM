#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : image
# @Time         : 2023/8/25 14:56
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from tempfile import SpooledTemporaryFile

from unstructured.partition import pdf
from unstructured.partition.text import partition_text


def get_ocr_text(file=None, filename=None):
    try_import('rapidocr_onnxruntime')

    from rapidocr_onnxruntime import RapidOCR

    ocr_fn = RapidOCR()  # 增加api逻辑
    result, elapse = ocr_fn(file or filename)
    text = [r[1] for r in result]
    text = '\n'.join(text)
    return text


def _partition_pdf_or_image_with_ocr(
    filename: str = "",
    file: Optional[Union[bytes, typing.BinaryIO, SpooledTemporaryFile]] = None,
    include_page_breaks: bool = False,
    ocr_languages: str = "eng",
    is_image: bool = False,
    max_partition: Optional[int] = 1500,
    min_partition: Optional[int] = 0,
    metadata_last_modified: Optional[str] = None,
):
    """Partitions and image or PDF using RapidOCR. For PDFs, each page is converted
    to an image prior to processing."""

    if is_image:
        text = get_ocr_text(file or filename)

        elements = partition_text(
            text=text,
            max_partition=max_partition,
            min_partition=min_partition,
            metadata_last_modified=metadata_last_modified,
        )

    else:
        elements = pdf._partition_pdf_or_image_with_ocr(
            filename, file, include_page_breaks, ocr_languages, is_image, max_partition, min_partition,
            metadata_last_modified
        )
    return elements


pdf._partition_pdf_or_image_with_ocr = _partition_pdf_or_image_with_ocr  # 重写方法

from langchain.document_loaders import UnstructuredImageLoader

if __name__ == '__main__':
    from chatllm.llmchain.document_loaders import UnstructuredImageLoader

    loader = UnstructuredImageLoader(
        "/Users/betterme/PycharmProjects/AI/MeUtils/meutils/ai_cv/invoice.jpg",
        strategy='ocr_only'
    )
    data = loader.load()
    print(data)
