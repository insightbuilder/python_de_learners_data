window.addEventListener("DOMContentLoaded", () => {
    const websy = new WebSocket("ws://localhost:7555/")

    document.querySelector("#clicker").addEventListener("click", () =>{
        const textstr = document.querySelector("#payload").value
        websy.send(JSON.stringify({payload: textstr}))
    })

    websy.onmessage = ({ data }) => {
        const reply = JSON.parse(data)
        if (reply.counts) {
            document.querySelector("#cnt").textContent = data 
        }
        else {
            document.querySelector("#out").textContent = data 
        }
    }
})