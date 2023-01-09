let url = `ws://${window.location.host}/ws/socket-server/`
let form = document.getElementById('chat-form')
const main = document.getElementById('main')

const chatSocket = new WebSocket(url)

chatSocket.onopen = () => {
    console.log("Websocket connection established");
}

form.addEventListener('submit', (e) => {
    e.preventDefault()
    let msg = e.target.message.value
    console.log(msg)
    chatSocket.send(JSON.stringify({
        'message': msg
    }))

    form.reset()
})

chatSocket.onmessage = (e) => {
    let data = JSON.parse(e.data);
    console.log(data)
    
    addMessage(data['message'])
}

function addMessage(data) {
    const div = document.createElement('div');
    const p = document.createElement('p');

    p.innerText = data;
    div.appendChild(p);

    main.appendChild(div);
}