from langchain.document_loaders import PyPDFLoader


def get_pages(pdf_path: str) -> list:
    """This function parse digital pdf and returns pages"""
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    return pages
