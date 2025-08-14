document.addEventListener('DOMContentLoaded', () => {

    const tenantId = 1 ;

    function addMessageToBox(data) {
        const visitorMessage = `
            <p class="card-text text-break bg-primary-subtle rounded shadow p-2 visitor">
                ${data.message}
            </p>
        `;
        const systemMessage = `
            <p class="card-text text-break bg-warning-subtle rounded shadow p-2 system">
                ${data.message}
            </p>
        `;

        const chatMessages = document.getElementById("chatMessages");
        chatMessages.innerHTML += data.sender == "visitor" ? visitorMessage : systemMessage;
        
        chatMessages.scrollTo({
            top: chatMessages.scrollHeight,
            behavior: "smooth"
        });

    };

    const socket = new WebSocket(`ws://localhost:8000/ws/chat/1o4n635m3q4l0r3p0f6g5l/`);

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        addMessageToBox(data);
    };

    const sendMessage = document.getElementById('sendMessage');
    if (sendMessage) {
        sendMessage.addEventListener('submit', function(event) {
            event.preventDefault();
            let data = new FormData(sendMessage);
            let message = data.get("message");
            socket.send(JSON.stringify({ message: message, sender: "system", tenant: tenantId }));
            sendMessage.reset();
        });
    };

});