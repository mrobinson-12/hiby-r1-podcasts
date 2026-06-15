const pathname = window.location.pathname;
const slug = pathname.split('/').pop();
const homebutton = document.getElementById("home-button")//TODO: add in prod somewhere
const uploadbutton = document.getElementById("upload-button")
const deletebutton = document.getElementById("delete-button")
const img = document.getElementById("podcast-image")
const podname = document.getElementById("podcast-title")
const desc = document.getElementById("podcast-description")

document.addEventListener('DOMContentLoaded', () => {
    fetch("/podcast/metadata?slug=" + slug)
        .then(response => response.text())
        .then(data => {
            const [name, description, url, slug, rss] = JSON.parse(data);
            img.src = url
            podname.textContent = name
            desc.textContent = description
            globalThis.rss = rss
            globalThis.ep = []
            return fetch("/podcast/recent?url=" + rss);
            })
            .then(response => response.text())
            .then(data => {
                const episodes = JSON.parse(data);
                const list = document.getElementById("episodes")
                episodes.forEach(({title, url }) => {
                    const episode = document.createElement("li")
                    episode.textContent = title
                    episode.className = "font-bold"
                    list.appendChild(episode)
                    ep.push({url, title})
                });
            });
});

//homebutton.addEventListener("click", () => {
  //  window.location.href = "/"
//})

uploadbutton.addEventListener("click", async () => {
    console.log("Uploading episodes...")//TODO: Remove in prod
    for (const {url, title} of ep.slice().reverse()) {
        response = await fetch("/podcast/upload?url=" + url + "&name=" + title + "&rss=" + rss)
        console.log(response.status)//TODO: Remove in prod
    }
    console.log("Episodes uploaded!")
})

deletebutton.addEventListener("click", async () => {
    console.log("Deleting podcast.")
    response = await fetch("/podcast/delete?url=" + rss, {})
    //For debugging purposes. TODO: Take away in prod
    console.log(response.status)
    window.location.href = "/"
})
