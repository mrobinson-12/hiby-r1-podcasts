from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
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
@app.get("/podcast/delete")
def deletepodcast(url: str = Query(...)):
    return codething.deletepodcast(url)
@app.get("/podcast/new")
def upload(url: str = Query(...)):
    return codething.addpodcast(url)

@app.get("/podcast/metadata")
def getmetadata(slug: str = Query(...)):
    return codething.getpodcast(slug)

@app.get("/podcast/upload")
def upload(url: str = Query(...), name: str = Query(...), rss: str = Query(...)):
    return codething.upload(url, name, rss)

@app.get("/podcast/get")
def getpodcasts():
    return codething.getpodcasts()

@app.get("/podcast/{name}")
async def podcast_page(name: str):
    if name.endswith(".js") or name.endswith(".css") or name.endswith("delete"):
        return FileResponse(name)
    return FileResponse("frontend/podcast.html")

@app.get("/")
async def serve_index():
    return FileResponse("frontend/index.html")



app.mount("/static", StaticFiles(directory="frontend"), name="static")