from pydantic import BaseModel


class DownloadInfo(BaseModel):
  url: str

class Chat(BaseModel):
  question: str
