from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import codething
from fastapi import FastAPI
from fastapi import Query
app = FastAPI()
# This is the fastapi file which serves the api for the frontend.

# Pings audiobookshelf
@app.get("/ping")
def ping():
    return {"status": codething.pingaudiobookshelf().status_code}

# Gets the recent episodes of a podcast
@app.get("/podcast/recent")
def getepisode(url: str = Query(...)):
    return codething.getrecentepisodes(url)

# Deletes a podcast
@app.get("/podcast/delete")
def deletepodcast(url: str = Query(...)):
    return codething.deletepodcast(url)

# Adds a podcast
@app.get("/podcast/new")
def upload(url: str = Query(...)):
    return codething.addpodcast(url)

# Gets the metadata of a podcast
@app.get("/podcast/metadata")
def getmetadata(slug: str = Query(...)):
    return codething.getpodcast(slug)

# Uploads a podcast
@app.get("/podcast/upload")
def upload(url: str = Query(...), name: str = Query(...), rss: str = Query(...)):
    return codething.upload(url, name, rss)

# Gets all podcasts metadata
@app.get("/podcast/get")
def getpodcasts():
    return codething.getpodcasts()

# Serves the podcast page
@app.get("/podcast/{name}")
async def podcast_page(name: str):
    if name.endswith(".js") or name.endswith(".css") or name.endswith("delete"):
        return FileResponse(name)
    return FileResponse("frontend/podcast.html")

# Serves the home page
@app.get("/")
async def serve_index():
    return FileResponse("frontend/index.html")


# Does some static file serving thing
app.mount("/static", StaticFiles(directory="frontend"), name="static")