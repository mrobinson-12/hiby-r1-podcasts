response = document.getElementById("response")
getbutton = document.getElementById("get")
addbutton = document.getElementById("add-new")

document.addEventListener('DOMContentLoaded', () => {
    getbutton.click()
})


getbutton.addEventListener("click", () => {
    document.getElementById("podcasts").innerHTML = '';
    fetch("/podcast/get")
        .then(response => response.text())
        .then(data => {
            images = JSON.parse(data)
            images.forEach(([id, title, description, image]) => {
                div=document.createElement("a")
                div.href="/podcast/"+id
                img1 = document.createElement("img")
                img1.src = image
                img1.className="w-48 mr-2"
                //text=document.createElement("p")
                //text.textContent=name
                //text.className="mr-2"
                div.appendChild(img1)
                //div.appendChild(text)

                document.getElementById("podcasts").appendChild(div)
            })
        })
})

addbutton.addEventListener("click", () => {
    const id = prompt("Enter the id:")
    fetch("/podcast/new?id="+id, {
        method: "GET"
    })
        .then(response => response.text())
        .then(data => {
            response.textContent = data
            sleep(1000)
            location.reload()
        })
})

//TODO UI Redo
//TODO Add searching