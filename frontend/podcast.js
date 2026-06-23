const pathname = window.location.pathname;
const slug = pathname.split('/').pop();
const uploadbutton = document.getElementById("upload-button")
const deletebutton = document.getElementById("delete-button")
const img = document.getElementById("podcast-image")
const podname = document.getElementById("podcast-title")
const desc = document.getElementById("podcast-description")
const list = document.getElementById("episodes")
function looksLikeHTML(str) {
    return /<[^>]+>|&(amp|lt|gt|quot|#39);/.test(str);
}
function getrecent() {
    list.replaceChildren()
    return fetch("/podcast/recent?url=" + rss)
    .then(response => response.text())
    .then(data => {
        const episodes = JSON.parse(data);
        episodes.forEach(({title, url }) => {
            const episode = document.createElement("li")
            episode.textContent = title
            episode.className = "font-bold"
            list.appendChild(episode)
            ep.push({url, title})
        });
    });
}
function getmeta() {
    podname.textContent = "Loading..."
    desc.textContent = "Loading..."
        fetch("/podcast/metadata?slug=" + slug)
        .then(response => response.text())
        .then(data => {
            const [name, description, url, slug, rss] = JSON.parse(data);
            img.src = url
            podname.textContent = name
            if (looksLikeHTML(description)) {
                desc.innerHTML = description;
            } else {
                desc.textContent = description;
            }
            globalThis.rss = rss
            globalThis.ep = []
            getrecent()
            });

}
document.addEventListener('DOMContentLoaded', () => {
    getmeta()
});

//homebutton.addEventListener("click", () => {
  //  window.location.href = "/"
//})

uploadbutton.addEventListener("click", async () => {
    uploadbutton.textContent = "Uploading..."
    for (const {url, title} of ep.slice().reverse()) {
        response=await fetch("/podcast/upload?url=" + encodeURIComponent(url) + "&name=" + encodeURIComponent(title) + "&slug=" + encodeURIComponent(slug))
        uploadbutton.textContent = await response.text()
    }
    getrecent()
})
let confirmDelete = false;

deletebutton.addEventListener("click", async () => {
if (!confirmDelete) {
        confirmDelete = true;
        deletebutton.textContent = "Are you sure?";
        return;
    }
    await fetch("/podcast/delete?url=" + rss, {})
    window.location.href = "/"
})
