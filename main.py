from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import codething
from fastapi import FastAPI, BackgroundTasks
from fastapi import Query
import subprocess
import os
app = FastAPI()

# This is the fastapi file which serves the api for the frontend. (When it works)
@app.post("/webhook")
def webhook():
    subprocess.run(['bash', 'pull.sh'])
    return {"status": "Pulling"}
# Gets the recent episodes of a podcast
@app.get("/podcast/recent")
def getepisode(id: str = Query(...)):
    return codething.getrecentepisode(id)
@app.get("/podcast/recents")
def getepisode(id: str = Query(...)):
    return codething.getrecentepisodes(id)

@app.get("/podcast/delete")
def deletepodcast(id: str = Query(...)):
    return codething.deletepodcast(id)

# Adds a podcast
@app.get("/podcast/new")
def upload(id: str = Query(...)):
    return codething.addpodcast(id)

# Gets the metadata of a podcast
@app.get("/podcast/metadata")
def getmetadata(id: str = Query(...)):
    return codething.getpodcastinfo(id)

# Uploads a podcast
@app.get("/podcast/upload")
def upload(id: str = Query(...)):
    return codething.upload(id)

# Gets all podcasts metadata
@app.get("/podcast/get")
def getpodcasts():
    return codething.getpodcasts()

# Serves the podcast page
@app.get("/podcast/{id}")
async def podcast_page(id: int):
    if str(id).endswith(".js") or str(id).endswith(".css") or str(id).endswith("delete"):
        return FileResponse(id)
    return FileResponse("frontend/podcast.html")

@app.get("/settings")
async def settings(setting: str = Query(...), value: str = Query(...)):
    return codething.settings(setting, value)

@app.get("/setting")
async def settings():
    return FileResponse("frontend/settings.html")

# Serves the home page
@app.get("/")
async def serve_index():
    return FileResponse("frontend/index.html")


# Does some static file serving thing
app.mount("/static", StaticFiles(directory="frontend"), name="static")