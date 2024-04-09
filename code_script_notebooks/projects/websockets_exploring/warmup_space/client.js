// create a listener on the window
window.addEventListener("DOMContentLoaded", () => {
    const client = new WebSocket("ws://localhost:8002/")
    sendClicker()
})


function sendClicker() {
    document.addEventListener('click', () =>{
        
    }
}