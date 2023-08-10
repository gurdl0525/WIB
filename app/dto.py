from pydantic import BaseModel


class RequestCrawl(BaseModel):
    typ: str
    occ: str


class RequestShow(BaseModel):
    typ: str
    tag: str
    occ: str


class RequestCloudwords(BaseModel):
    occ: str
