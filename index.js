pingbutton = document.getElementById("ping")
response = document.getElementById("response")
getbutton = document.getElementById("get")
addbutton = document.getElementById("add-new")
pingbutton.addEventListener("click", () => {
    fetch("/ping")
        .then(response => response.text())
        .then(data => {
            response.textContent = data
        })
})

getbutton.addEventListener("click", () => {
    document.getElementById("podcasts").innerHTML = '';
    fetch("/podcast/get")
        .then(response => response.text())
        .then(data => {
            images = JSON.parse(data)
            images.forEach(([name, description, url, slug, rss]) => {
                div=document.createElement("a")
                div.href="/podcast/"+slug
                img = document.createElement("img")
                img.src = url
                img.className="w-48 mr-2"
                //text=document.createElement("p")
                //text.textContent=name
                //text.className="mr-2"
                div.appendChild(img)
                //div.appendChild(text)

                document.getElementById("podcasts").appendChild(div)
            })
        })
})

addbutton.addEventListener("click", () => {
    const rss = prompt("Enter the rss link:")
    fetch("/podcast/new?url="+rss, {
        method: "GET"
    })
        .then(response => response.text())
        .then(data => {
            response.textContent = data
        })
})