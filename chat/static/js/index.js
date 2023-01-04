console.log("Index Check");

document.querySelector('#roomInput').focus();

document.querySelector('#roomInput').onkeyup = (e) => {
    if(e.keyCode == 13) {
        document.querySelector('#roomConnect').click();
    }  
};

document.querySelector('#roomConnect').onclick = () => {
    let roomName = document.querySelector('#roomInput').value;
    window.location.pathname = '/room/'+ roomName;
};

document.querySelector('#roomSelect').onchange = () => {
    let roomName = document.querySelector('#roomSelect').value.split(' (')[0];
    window.location.pathname = '/room/'+ roomName;
};