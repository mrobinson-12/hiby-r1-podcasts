import codething
from fastapi import FastAPI
from fastapi import Query
app = FastAPI()

@app.get("/ping")
def ping():
    return {"status": codething.pingaudiobookshelf().status_code}

@app.get("/podcast/recent")
def getepisode(url: str = Query(...)):
    return codething.getrecentepisodes(url)

@app.get("/podcast/new")
def upload(url: str = Query(...)):
    return codething.addpodcast(url)

@app.get("/podcast/metadata")
def getmetadata(url: str = Query(...)):
    return codething.getpodcast(url)

