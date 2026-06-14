import requests
import os
import json
from urllib.parse import unquote
from dotenv import load_dotenv
from multiprocessing.pool import ThreadPool
import mimetypes
import re
load_dotenv()

def pingaudiobookshelf():
    response = requests.get(f"{os.environ.get("AUDIOBOOKSHELF_BASE_URL")}/ping")
    return response

def getdata():
    with open("podcasts.json", "r") as f:
        loaddata = json.load(f)
    return loaddata

def addpodcast(url):
    loaddata=getdata()
    with open("podcasts.json", "w") as f:
        loaddata["podcasts"][unquote(url)] = {"slug": f"{url.split("/")[-1]}", "last_episode": ""}
        json.dump(loaddata, f, indent=4)
    return "Podcast added"

def getpodcast(slug):
    if pingaudiobookshelf().status_code == 200:
        podcasts = getdata()["podcasts"]
        for url, data in podcasts.items():
            if data["slug"] == slug:
                rss=url
                break

        metadata=[]
        headers= {
            "Authorization": f"Bearer {os.environ.get('AUDIOBOOKSHELF_API_KEY')}",
            "Content-Type": "application/json"
        }
        data = {
            "rssFeed": rss
        }
        response = requests.post(f"{os.environ.get('AUDIOBOOKSHELF_BASE_URL')}/api/podcasts/feed", headers=headers, json=data)
        metadata.append(response.json()['podcast']['metadata']['title'])
        metadata.append(response.json()['podcast']['metadata']['description'])
        metadata.append(response.json()['podcast']['metadata']['image'])
        metadata.append(getdata()["podcasts"][rss]["slug"])
        metadata.append(rss)
        return metadata

def getrecentepisodes(url):

    loaddata=getdata()
    data=loaddata
    global rssurl
    rssurl=unquote(url)
    lastepisode=data["podcasts"][url]["last_episode"]
    headers= {
            "Authorization": f"Bearer {os.environ.get('AUDIOBOOKSHELF_API_KEY')}",
            "Content-Type": "application/json"
    }
    data = {
        "rssFeed": rssurl
    }
    response = requests.post(f"{os.environ.get('AUDIOBOOKSHELF_BASE_URL')}/api/podcasts/feed", headers=headers, json=data)
    episodes = response.json()['podcast']['episodes']
    recent = episodes[0]['title']
    print(lastepisode)
    #To Test

    if lastepisode != recent:
        recentepisodes = []
        for i, ep in enumerate(episodes):
            if lastepisode != ep['title']:
                recentepisodes.append({'title': ep['title'], "url": ep['enclosure']["url"]})
                continue
            else:
                print(type(recentepisodes), recentepisodes)
                return recentepisodes
        else:
            print(type(recentepisodes), recentepisodes)
            return [{'title':episodes[len(episodes)-1]['title'], "url": episodes[len(episodes)-1]['enclosure']["url"]}]
    else:
        return []


# TODO: Get uploading work most of the time
def upload(url, name, rss):
    loaddata=getdata()
    r = requests.get(url, stream=True, allow_redirects=True)
    content_type = r.headers.get("Content-Type", "").split(";")[0].strip()
    ext = mimetypes.guess_extension(content_type) or ".mp3"
    name = f"{name}{ext}"
    name = name.replace('\xa0', ' ').strip()
    name = re.sub(r'\.(mp3|m4a|ogg|aac|wav|flac)$', '', name)
    with open(name, "wb") as f:
        for chunk in r.iter_content(chunk_size=65536):
            f.write(chunk)
    requests.post("http://192.168.1.89:4399/upload", data={"path": "/data/mnt/sd_0/testing/Podcast/"}, files={"files[]": open(f"{name}.mp3", "rb")})
    loaddata["podcasts"][rss]["last_episode"] = name
    with open("podcasts.json", "w") as f:
        json.dump(loaddata, f, indent=4)
    os.remove(f"{name}.mp3")

def getpodcasts():
    loaddata=getdata()
    slugs = [data["slug"] for data in loaddata["podcasts"].values()]
    with ThreadPool() as pool:
        return pool.map(getpodcast, slugs)

