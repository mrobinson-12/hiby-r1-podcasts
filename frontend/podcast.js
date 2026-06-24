const pathname = window.location.pathname;
const id = pathname.split('/').pop();
const uploadbutton = document.getElementById("upload-button")
const deletebutton = document.getElementById("delete-button")
const img = document.getElementById("podcast-image")
const podname = document.getElementById("podcast-title")
const desc = document.getElementById("podcast-description")
const list = document.getElementById("episodes")

function getrecent() {
    list.replaceChildren()
    return fetch("/podcast/recents?id=" + id)
    .then(response => response.text())
    .then(data => {
        const episodes = JSON.parse(data);
        episodes.forEach((title) => {
            const episode = document.createElement("li")
            episode.textContent = title
            episode.className = "font-bold"
            list.appendChild(episode)
            ep.push(title)
        });
    });
}
function getmeta() {
    podname.textContent = "Loading..."
    desc.textContent = "Loading..."
        fetch("/podcast/metadata?id=" + id)
        .then(response => response.text())
        .then(data => {
            const [id, name, description, url] = JSON.parse(data);
            img.src = url
            podname.textContent = name
            desc.textContent = description
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
        response=await fetch("/podcast/upload?id=" + id)
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
    await fetch("/podcast/delete?id=" + id, {})
    window.location.href = "/"
})
