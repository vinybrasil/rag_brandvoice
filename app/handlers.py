import logging
from typing import Any

from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel
from unstructured.partition.pdf import partition_pdf


class Element(BaseModel):
    type: str
    payload: Any


logging.basicConfig(
    level=logging.INFO, format="%(levelname)s - %(asctime)s  - %(message)s"
)


def read_pdf(filename):
    raw_pdf_elements = partition_pdf(
        filename=filename,
        extract_images_in_pdf=False,
        infer_table_structure=True,
        strategy="hi_res",
        chunking_strategy="by_title",
        languages=["eng"],
        max_characters=2000,
        combine_text_under_n_chars=500,
    )

    category_counts = {}

    for element in raw_pdf_elements:
        category = str(type(element))
        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts[category] = 1

    categorized_elements = []
    for element in raw_pdf_elements:
        if "unstructured.documents.elements.Table" in str(type(element)):
            categorized_elements.append(Element(type="table", payload=str(element)))
        elif "unstructured.documents.elements.CompositeElement" in str(type(element)):
            categorized_elements.append(Element(type="text", payload=str(element)))

    text_elements = [e for e in categorized_elements if e.type == "text"]
    texts = [i.payload for i in text_elements]
    logging.info(f"Number of text chunks found: {len(text_elements)}")

    table_elements = [e for e in categorized_elements if e.type == "table"]
    tables = [i.payload for i in table_elements]
    logging.info(f"Number of tables chunks found: {len(table_elements)}")

    return texts, tables

def create_model(retriever):
    # template = """Context: You're an brand specialist that will speak with the 
    # brand guidelines given. You speak as the brand voice. The guidelines are the following:
    # {context}
    # Question: {question}
    # """
    template = """Context: You're a shoes brand that will speak with the 
    brand guidelines given. You speak as the brand, like in a commercial. You can
    anwser the question about products and the mission of the company. The guidelines are the following:
    {context}
    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    model = Ollama(model="llama3")

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    return chain