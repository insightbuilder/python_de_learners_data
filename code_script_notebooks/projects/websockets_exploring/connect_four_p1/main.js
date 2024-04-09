import { createBoard, playMove } from "./connect4.js";

window.addEventListener("DOMContentLoaded", () => {
  // Initialize the UI.
  const board = document.querySelector(".board");
  createBoard(board);
  const websocket = new WebSocket("ws://localhost:8001/")  // websocket client
  recieveMoves(board, websocket)
  sendMoves(board, websocket)
});


function sendMoves(board, websocket) {
    // Sends the message to server with websocket object
    board.addEventListener("click", ({ target }) =>{
        const column = target.dataset.column;
        if (column === undefined) {
            return;
        }
        const event = {
            type: 'play',
            column: parseInt(column, 10)
        };  // will take the input event and send the data
        websocket.send(JSON.stringify(event))
    });
}


function showMessage(message) {
    window.setTimeout(() => window.alert(message), 50)
}


function recieveMoves(board, websocket) {
    websocket.addEventListener("message", ({ data }) => {
        const event = JSON.parse(data)
        // verify the event type and take action
        switch (event.type) {
            case "play":
                playMove(board, event.player, event.column, event.row)
                break;

            case "win":
                showMessage(`Player ${event.player} winns!!!!`)
                websocket.close(1000);
                break;
            
            case "error":
                showMessage(event.message)
                break;

            default:
                throw new Error(`Not Supported ${event.type}`)

        }
    });
}