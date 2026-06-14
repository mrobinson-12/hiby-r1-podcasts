const pathname = window.location.pathname;
const slug = pathname.split('/').pop();
const homebutton = document.getElementById("home-button")
const uploadbutton = document.getElementById("upload-button")
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
    console.log("Uploading episodes...")
    for (const {url, title} of ep.slice().reverse()) {
        response = await fetch("/podcast/upload?url=" + url + "&name=" + title + "&rss=" + rss)
        console.log(response.status)
    }
    console.log("Episodes uploaded!")
})
