window.addEventListener("DOMContentLoaded", () =>{
    const websy = new WebSocket("ws://localhost:7568/");

    document.querySelector("#reply").addEventListener("click", () => {
        const sys_prompt = document.querySelector("#syspt").value
        const user_prompt = document.querySelector("#userpt").value
        websy.send(JSON.stringify({sys_prompt:sys_prompt,
                                    user_prompt:user_prompt}))
    });
    
    document.querySelector("#dbin").addEventListener("click", () => {
        websy.send(JSON.stringify({need_data:'database data'}))
    });

    websy.onmessage = ({ data }) => {
        const json_data = JSON.parse(data)
        if ('output' in json_data) {
            const reply = json_data['output']
            document.querySelector("#llm_reply").textContent = reply 
        }
        if ('ptbl' in json_data) {
            const tbl_data = json_data['ptbl']
            console.log(tbl_data.length)
            tbl_data.forEach(element => {
                console.log(element)
                document.querySelector("#dbout").innerHTML += `
                <div>
                    <p><span>User Prompt: </span>${element['user_prompt']}</p>
                    <p><span>LLM Reply: </span>${element['llm_reply']}</p>
                </div>
                `
            });
        }
    }
})