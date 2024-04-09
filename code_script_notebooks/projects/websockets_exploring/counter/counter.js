window.addEventListener("DOMContentLoaded", () =>{
    const websy = new WebSocket("ws://localhost:7777/");

    document.querySelector(".minus").addEventListener("click", () =>{
        websy.send(JSON.stringify({action: "minus"}));
    });
    
    document.querySelector(".plus").addEventListener("click", () =>{
        websy.send(JSON.stringify({action: "plus"}));
    });

    websy.onmessage = ({ data }) => {
        const event = JSON.parse(data);
        switch (event.type) {
            case "value":
                document.querySelector(".value").textContent = event.value;
                break;
            
            case "users":
                const users = `${event.count} user${event.count == 1 ? "" : "s"}`;
                document.querySelector(".users").textContent = users;
                break

            default:
                console.error(`Unsupported: ${event}`)
        }
    }
})