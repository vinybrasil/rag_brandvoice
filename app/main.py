from fastapi import FastAPI, HTTPException
from tempfile import TemporaryDirectory
import pathlib
import requests
from app.schemas import DownloadInfo
from app.handlers import read_pdf

app = FastAPI()

@app.get("/api/v1/health")
async def health_check():
    return {"message": "alive"}

@app.get("/api/v1/download")
async def download_file(download_info: DownloadInfo):
    try:
        with TemporaryDirectory() as dirname:
            filename = str(pathlib.Path(dirname) / "input.pdf")
            print(filename)
            # url = "https://a.slack-edge.com/a29fb/marketing/img/media-kit/Slack-Brand-Guidelines.pdf"
            response = requests.get(download_info.url, stream=True)
            response.raise_for_status()

            with open(filename, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            texts, tables = read_pdf(filename)
                    
            
            return {"message": texts[0]}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to download file: {str(e)}")

