let url = `ws://${window.location.host}/ws/socket-server/`

const chatSocket = new WebSocket(url)

chatSocket.onopen = () => {
    console.log("Websocket connection established");
}

chatSocket.onmessage = (e) => {
    let data = JSON.parse(e.data);
    console.log(data)
}