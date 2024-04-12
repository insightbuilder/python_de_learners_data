window.addEventListener("DOMContentLoaded", () => {
    const websy = new WebSocket("ws://localhost:7555/")

    document.querySelector("#clicker").addEventListener("click", () =>{
        const textstr = document.querySelector("#payload").value
        websy.send(JSON.stringify({payload: textstr}))
    })

    websy.onmessage = ({ data }) => {
        const reply = JSON.parse(data)
        if ('packet' in reply) {
            document.querySelector("#trg").innerHTML += `<li>${reply['packet']}</li>` 
        }
    }
})