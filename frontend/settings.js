keything=document.getElementById("api-key").value;
urlthing=document.getElementById("url").value;
b1=document.getElementById("save-settings-1");
b2=document.getElementById("save-settings-2");

//TODO Fix this cause idk what its doing
b1.addEventListener("click", () => {
fetch("/settings?setting=hiby-url&value="+urlthing)
})

b2.addEventListener("click", () => {
fetch("/settings?setting=api-key&value="+keything)
})