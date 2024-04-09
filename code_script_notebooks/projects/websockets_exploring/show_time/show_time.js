window.addEventListener("DOMContentLoaded", () => {
    const messages = document.createElement("ul");
    document.body.append(messages)

    const websy = new WebSocket("ws://localhost:5678/")
    websy.onmessage = ({ data }) => {
        const message = document.createElement('li')
        const content = document.createTextNode(data)
        message.appendChild(content)
        messages.appendChild(message)
    };
});