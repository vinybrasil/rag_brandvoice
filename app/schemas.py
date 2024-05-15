from pydantic import BaseModel

class DownloadInfo(BaseModel):
  url: str
