const CSRF = document.currentScript.dataset.csrf
const inputs = document.querySelectorAll("input");
const username = document.querySelector("#username");
const title = document.querySelector("#title");
const text = document.querySelector("#text");

document.addEventListener("DOMContentLoaded", function(e){
    if (localStorage.getItem("username")){
        username.remove()
    }
})

document.querySelector("form").addEventListener("submit", function(e){
    e.preventDefault()
    let getUsername = localStorage.getItem("username")
    if(getUsername == null ){
        localStorage.setItem("username", username.value)
    }
    const sendReqest = async ()=> {
        if(title.value === "" && text.value === ""){
            alert("Error")
            return
        }
        const response = await fetch("http://127.0.0.1:8000/api/create", {
            "method": "POST",
            "body": JSON.stringify({"username": localStorage.getItem("username"), "title": title.value, "text": text.value})
        })
        const sendData = await response.json()
        console.log(sendData)
        if(!sendData['Error']){
        location.href = `/posts/${sendData.slug}/`
        //localStorage.setItem("username", username.value)
        }else{
            alert(`${sendData['Error']}`)
        }
    }
    sendReqest()
})