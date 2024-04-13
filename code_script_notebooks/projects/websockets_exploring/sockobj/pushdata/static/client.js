window.addEventListener("DOMContentLoaded", () => {
    const websy = new WebSocket("ws://localhost:7568/");

    document.querySelector("#tap").addEventListener("click", () => {
       console.log("Got clcic...") 
       websy.send('data')
    })
    
    document.querySelector("#notap").addEventListener("click", () => {
        console.log('closing?? ')
        websy.send('close')
    })
    websy.onmessage = ({ data }) => {
        document.querySelector("#place").innerHTML += `<li>${data}</li>`
    }
})