import io
import pypdf
import docx
import json

def process_pdf(contents: bytes) -> str:
    """Extract text from PDF file."""
    reader = pypdf.PdfReader(io.BytesIO(contents))
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def process_docx(contents: bytes) -> str:
    """Extract text from DOCX file."""
    doc = docx.Document(io.BytesIO(contents))
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text


def process_json(contents: bytes) -> str:
    """Process JSON and extract relevant fields (could be customized)."""
    data = json.loads(contents)
    return json.dumps(data) 