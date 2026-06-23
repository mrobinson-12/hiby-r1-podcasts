import subprocess

import requests
import os
import json
from urllib.parse import unquote
from dotenv import load_dotenv
from multiprocessing.pool import ThreadPool
import mimetypes
import re
# Load envs
load_dotenv()
# Pings audiobookshelf
def pingaudiobookshelf():
    response = requests.get(f"{os.environ.get('AUDIOBOOKSHELF_BASE_URL')}/ping")
    return response

#gets all podcasts
def getdata():
    with open("podcasts.json", "r") as f:
        loaddata = json.load(f)
    return loaddata

#adds a podcast to the database
def addpodcast(url):
    loaddata=getdata()
    response=requests.post(f"{os.environ.get('AUDIOBOOKSHELF_BASE_URL')}/api/podcasts/feed", json={"rssFeed": url}, headers={"Authorization": f"Bearer {os.environ.get('AUDIOBOOKSHELF_API_KEY')}"})
    title=(response.json()['podcast']['metadata']['title'])
    title=title.replace(" ", "-")
    title = title.replace("&", "and")
    title = title.replace("/", "-")
    title = title.replace(":", "")
    title = title.replace("?", "")
    title = title.replace(",", "")
    title = title.replace(".", "")
    with open("podcasts.json", "w") as f:
        loaddata["podcasts"][unquote(url)] = {"slug": title, "last_episode": ""}
        json.dump(loaddata, f, indent=4)
    return "Podcast added"

#gets metadata of a podcast
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

#gets recent episodes of a podcast
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

def upload(url, name, slug):
    loaddata=getdata()
    r = requests.get(url, stream=True, allow_redirects=True)
    content_type = r.headers.get("Content-Type", "").split(";")[0].strip()
    ext = mimetypes.guess_extension(content_type) or ".mp3"
    name1=re.sub(r'[\\/:*?"<>|#&]', "-", name).strip()
    name = f"{name}{ext}"
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
    rss=getpodcast(slug)[4]
    loaddata["podcasts"][rss]["last_episode"] = name
    with open("podcasts.json", "w") as f:
        json.dump(loaddata, f, indent=4)
    os.remove(f"{name}")
    os.remove(f"{name1}.mp3")
    return name1 + " Uploaded"

# Gets all podcasts
def getpodcasts():
    loaddata=getdata()
    slugs = [data["slug"] for data in loaddata["podcasts"].values()]
    with ThreadPool() as pool:
        return pool.map(getpodcast, slugs)

# Deletes a podcast
def deletepodcast(url):
    loaddata=getdata()
    if url in loaddata["podcasts"]:
        loaddata["podcasts"].pop(url)
        with open("podcasts.json", "w") as f:
            json.dump(loaddata, f, indent=4)
            return "Podcast deleted"
    return "Podcast not found"

def settings(setting, value):
    if setting == "hiby-url":
        os.environ["HIBY_URL"] = value
    if setting == "api-key":
        os.environ["AUDIOBOOKSHELF_API_KEY"] = value

