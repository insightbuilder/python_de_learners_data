window.addEventListener("DOMContentLoaded", () =>{
    const websy = new WebSocket("ws://localhost:7568");

    document.querySelector("#click").addEventListener("click", () =>{
        const in_data = document.querySelector("#in").value
        websy.send(JSON.stringify({input: in_data}))
    })

    document.querySelector("#db").addEventListener("click", () =>{
        const in_data = {database:'give'}
        websy.send(JSON.stringify(in_data))
    })

    websy.onmessage = ({ data }) => {
        out_data = JSON.parse(data)
        console.log(out_data)
        if ('output' in out_data) {
            document.querySelector("#out").textContent = out_data['output']
        }
        else if ('db_data' in out_data) {
            array_data = out_data['db_data']
            document.querySelector("#data").innerHTML = ""
            array_data.forEach(element => {
                console.log(element) 
                document.querySelector("#data").innerHTML +=`<tr>
                    <td scope="col">${element["input_text"]}</td>
                    <td scope="col">${element["output_text"]}</td>
                </tr>
                `
            })
        }
    }
})