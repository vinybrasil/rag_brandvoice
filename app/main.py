import pathlib
import uuid
from tempfile import TemporaryDirectory

import requests
from fastapi import FastAPI, HTTPException
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.storage import InMemoryStore
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from app.handlers import create_model, read_pdf
from app.schemas import Chat, DownloadInfo

app = FastAPI()

@app.get("/api/v1/health")
async def health_check():
    return {"message": "alive"}

@app.get("/api/v1/download")
async def download_file(download_info: DownloadInfo):
    try:
        with TemporaryDirectory() as dirname:
            filename = str(pathlib.Path(dirname) / "input.pdf")
            #print(filename)
            # url = "https://a.slack-edge.com/a29fb/marketing/img/media-kit/Slack-Brand-Guidelines.pdf"
            response = requests.get(download_info.url, stream=True)
            response.raise_for_status()

            with open(filename, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            filename = "/home/vinybrasil/random_projects/nuvia/rag_multimodal/data/Slack-Brand-Guidelines_voice.pdf"

            texts, tables = read_pdf(filename)

            doc_ids = [str(uuid.uuid4()) for _ in texts]
            summary_texts = [
                Document(page_content=s, metadata={id_key: doc_ids[i]})
                for i, s in enumerate(texts)
            ]
            retriever.vectorstore.add_documents(summary_texts)
            retriever.docstore.mset(list(zip(doc_ids, texts))) 
            
            return {"message": texts[0]}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to download file: {str(e)}")

@app.get("/api/v1/chat")
async def ask_question(question: Chat):
    chain = create_model(retriever)
    res = chain.invoke(question.question)
    return {"message": res}

store = InMemoryStore()
id_key="doc_id"

embedding = FastEmbedEmbeddings()
vectorstore = Chroma(
    collection_name="summaries11",
    embedding_function=embedding,
)

retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    docstore=store,
    id_key=id_key,
)