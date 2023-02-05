const roomName = JSON.parse(document.getElementById('roomName').textContent);
const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/${roomName}/`);
const chatArea = document.getElementById('chatArea');
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');

chatSocket.onmessage = (e) => {
    const data = JSON.parse(e.data);
    if(data.type == 'chat') {
        var para = document.createElement('p');
        para.innerHTML += `${data.from}: ${data.message}\n`;
        chatArea.appendChild(para);
    }
    else if (data.type == 'question')
    {
        var previousQues = document.getElementsByClassName('question');
        console.log(previousQues);
        if(previousQues.length > 0) {
            previousQues[0].remove();
        }

        var questionDiv = document.createElement('div');
        questionDiv.className = 'question';

        var img = document.createElement('img');
        img.src = data.flag_url;

        questionDiv.appendChild(img);

        var optionForm = document.createElement('form');
        optionForm.id = 'questionForm';
        var options = data.options;

        options.forEach((option)=>{
            var optionNode = document.createElement('input');
            optionNode.type = 'radio';
            optionNode.name = 'option';
            optionNode.value = option;

            var label = document.createElement('label');
            label.htmlFor = option;

            label.innerText = option;

            optionForm.appendChild(optionNode);
            optionForm.appendChild(label);
        });

        var submitAns = document.createElement('input');
        submitAns.type = 'submit';
        submitAns.id = 'submitAnwer';

        optionForm.appendChild(submitAns);

        optionForm.addEventListener('submit', (e) => {
            e.preventDefault();

            var options = document.getElementsByName('option');
        
            options.forEach((opt) => {
                if(opt.checked)
                    chatSocket.send(JSON.stringify({
                        'type': 'response',
                        'value': opt.value
                    }));
            })
        });

        questionDiv.appendChild(optionForm);
        chatArea.appendChild(questionDiv);
    }
}

function submitResponse(e) {

}

chatForm.addEventListener('submit', (e) => {
        e.preventDefault();

        let message = e.target.messageInput.value.trim();
        chatSocket.send(JSON.stringify({
            'type': 'message',
            'message': message
        }));

        messageInput.value = "";
    });
