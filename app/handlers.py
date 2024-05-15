import logging


#from app.schemas import Element
from pydantic import BaseModel
from typing import Any

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


#texts, tables = read_pdf('/home/vinybrasil/random_projects/nuvia/rag_multimodal/data/Slack-Brand-Guidelines_voice.pdf')

# file://///wsl.localhost/Ubuntu/home/vinybrasil/random_projects/nuvia/rag_multimodal/data/Slack-Brand-Guidelines_voice.pdf
#breakpoint()