import hashlib
import json
import mimetypes
import os
import re
import subprocess
import time

import requests
from dotenv import load_dotenv

load_dotenv()

def authpi():
    apikey = os.environ.get("PODCAST_INDEX_KEY")
    apisecret = os.environ.get("PODCAST_INDEX_SECRET")
    apitime = str(int(time.time()))
    auth_string = apikey + apisecret + str(apitime)
    api_hash = hashlib.sha1(auth_string.encode("utf-8")).hexdigest()
    headers = {
        "User-Agent": "Mp3SyncThing/0.1",
        "X-Auth-Key": apikey,
        "X-Auth-Date": apitime,
        "Authorization": api_hash,
    }
    return headers

def getdata():
    with open("podcasts.json", "r") as f:
        loaddata = json.load(f)
        return loaddata
def addpodcast(id):
    data=getdata()
    data["podcasts"][str(id)] = {
        "last_episode_time": 0
    }
    with open("podcasts.json", "w") as f:
        json.dump(data, f, indent=4)


def getpodcastinfo(id):
    response=requests.get(f"https://api.podcastindex.org/api/1.0/podcasts/byfeedid?id={id}", headers=authpi())
    response.raise_for_status()
    info=[id, response.json()["feed"]["title"], response.json()["feed"]["description"], response.json()["feed"]["artwork"]]
    return info

def getrecentepisode(id):
    lasttime=getdata()["podcasts"][id]["last_episode_time"]
    response=requests.get(f"https://api.podcastindex.org/api/1.0/episodes/byfeedid?id={id}&since={lasttime}&max=1", headers=authpi())
    response.raise_for_status()
    episodes=response.json()["items"]
    episode=(episodes)[0]["title"], episodes[0]["enclosureUrl"], episodes[0]["datePublished"]
    return episode

def getrecentepisodes(id):
    lasttime=getdata()["podcasts"][id]["last_episode_time"]
    response=requests.get(f"https://api.podcastindex.org/api/1.0/episodes/byfeedid?id={id}&since={lasttime}&max=10", headers=authpi())
    response.raise_for_status()
    episodes=response.json()["items"]
    episodes.reverse()
    episodeslist=[]
    for episode in episodes:
        episodeslist.append(episode["title"])
    return episodeslist

def getpodcasts():
    loaddata=getdata()
    info=[]
    for infos in loaddata["podcasts"]:
        info.append(getpodcastinfo(infos))
    return info

def upload(id):
    loaddata=getdata()
    episodes=getrecentepisode(id)
    title=episodes[0]["title"]
    url=episodes[0]["enclosureUrl"]
    datepublished=episodes[0]["datePublished"]

    r=requests.get(url, stream=True, allow_redirects=True)
    content_type = r.headers.get("Content-Type", "").split(";")[0].strip()
    ext = mimetypes.guess_extension(content_type) or ".mp3"
    name1=re.sub(r'[\\/:*?"<>|#&]', "-", title).strip()
    name = f"{title}{ext}"
    name = re.sub(r'[\\/:*?"<>|#&ea]', "l", name).strip()
    with open(name, "wb") as f:
        for chunk in r.iter_content(chunk_size=65536):
            f.write(chunk)
    subprocess.run([
        "ffmpeg",
        "-i", name,
        "-ar", "16000",
        "-ac", "1",
        "-c:a", "libmp3lame",
        f"{name1}.mp3"
    ], check=True)
    requests.post(f"http://{os.environ.get('HIBY_URL')}:4399/upload", data={"path": "/data/mnt/sd_0/testing/Podcast/"}, files={"files[]": open(f"{name1}.mp3", "rb")})
    loaddata["podcasts"][id]["last_episode_time"] = datepublished
    with open("podcasts.json", "w") as f:
        json.dump(loaddata, f, indent=4)
    os.remove(f"{name}")
    os.remove(f"{name1}.mp3")
    return name1 + " Uploaded"

def deletepodcast(id):
    loaddata=getdata()
    if id in loaddata["podcasts"]:
        loaddata["podcasts"].pop(id)
        with open("podcasts.json", "w") as f:
            json.dump(loaddata, f, indent=4)
            return "Podcast deleted"
    return "Podcast not found"

#TODO: Add settings
