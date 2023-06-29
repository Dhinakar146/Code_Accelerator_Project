from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings


def get_data(pages: list, question: str, k=2, char_limit=500) -> str:
    """This function gets similar data from pages"""
    output = ""
    faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings())
    docs = faiss_index.similarity_search(question, k=k)
    for doc in docs:
        output = output + '\n' + doc.page_content[:char_limit]
    return output
