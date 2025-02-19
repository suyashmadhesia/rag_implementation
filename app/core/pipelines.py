from .base import BasePipeline
from app.utils.media_utils import *


class PDFIngestionPipeline(BasePipeline):

    def _process_file(self, contents):
        return process_pdf(contents)
    


class DocxIngestionPipeline(BasePipeline):

    def _process_file(self, contents):
        return process_docx(contents)
    


class TextIngestionPipeline(BasePipeline):

    def _process_file(self, contents):
        return contents.decode("utf-8")
    


class JSONIngestionPipeline(BasePipeline):

    def _process_file(self, contents):
        return process_json(contents)