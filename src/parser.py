from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def extract_text_from_docx(file):
    document = Document(file)
    text = ""

    for paragraph in document.paragraphs:
        if paragraph.text:
            text += paragraph.text + "\n"

    return text


def extract_text_from_txt(file):
    return file.read().decode("utf-8")


def extract_text(file):
    file_name = file.name.lower()

    if file_name.endswith(".pdf"):
        return extract_text_from_pdf(file)

    if file_name.endswith(".docx"):
        return extract_text_from_docx(file)

    if file_name.endswith(".txt"):
        return extract_text_from_txt(file)

    raise ValueError("Unsupported file type. Please upload PDF, DOCX, or TXT.")