import requests
import os
import json
from urllib.parse import unquote
from dotenv import load_dotenv
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
        loaddata["podcasts"][unquote(url)] = {"last_episode": ""}
        json.dump(loaddata, f, indent=4)
    return "Podcast added"

def getpodcast(url):
    if pingaudiobookshelf().status_code == 200:
        metadata=[]
        headers= {
            "Authorization": f"Bearer {os.environ.get('AUDIOBOOKSHELF_API_KEY')}",
            "Content-Type": "application/json"
        }
        data = {
            "rssFeed": url
        }
        response = requests.post(f"{os.environ.get('AUDIOBOOKSHELF_BASE_URL')}/api/podcasts/feed", headers=headers, json=data)
        metadata.append(response.json()['podcast']['metadata']['title'])
        metadata.append(response.json()['podcast']['metadata']['image'])
        return metadata

def getrecentepisodes(url):
    if pingaudiobookshelf().status_code == 200:
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
                    recentepisodes.append(ep['title'])
                    continue
                else:
                    return recentepisodes
            else:
                return episodes[len(episodes)-1]['title']
        else:
            return "No recent episodes"
    else:
        return "Audiobookshelf is offline"

def upload(url, name):
    loaddata=getdata()
    r = requests.get(url)
    with open(f"{name}.mp3", "wb") as f:
        for chunk in r.iter_content(chunk_size=1):
            f.write(chunk)
    requests.post("http://192.168.1.89:4399/upload", data={"path": "/data/mnt/sd_0/testing/Podcast/"}, files={"files[]": open(f"{name}.mp3", "rb")})
    loaddata["podcasts"][rssurl]["last_episode"] = name
    with open("podcasts.json", "w") as f:
        json.dump(loaddata, f, indent=4)
    #os.remove(f"{name}.mp3")


