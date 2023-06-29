from langchain.llms import OpenAI
from langchain.chains import LLMChain
from utils.prompts import prefix_prompt
from langchain.prompts import PromptTemplate


def generate_response(data: str, question: str) -> str:
    """This function generates response from data and question using openai llm"""
    llm = OpenAI(temperature=0.9)
    prompt = PromptTemplate(
        input_variables=["sources", "question"],
        template=prefix_prompt,
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run({"sources": data, "question": question})
