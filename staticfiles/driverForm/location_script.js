document.addEventListener('DOMContentLoaded', () => {
    const ipElements = document.querySelectorAll('.ip_addr');
    if (ipElements.length === 0) {
        console.warn('No hospital elements found with class .ip_addr');
        return;
    }

    const ip_addr = ipElements[0].dataset.ip;
    const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    fetch('/driverForm/receive_ip/', {
        method:'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ ip: ip_addr })
    })
    .then(response => response.json())
    .then(data => {
        if(data.error){
            console.error('server error:', data.error);
            return;
        }

        const { hospital_id,ip_addr } = data;

        const socket = new WebSocket(`ws://${window.location.hostname}:8000/ws/notify/${hospital_id}/`);

        socket.onopen = function(){
            console.log('WebSocket connection opened. Sending emergency info...');
            socket.send(JSON.stringify({
                emergency: "Heart Attack",
                latitude: "17.385044",
                longitude: "78.486671"
            }));
        };

        socket.onmessage = function (event) {
            const message = JSON.parse(event.data);
            alert("Hospital says: " + message.message);
        };

        socket.onerror = function (e) {
            console.error("WebSocket error:", e);
        };
    })
    .catch(error => {
        console.error('error :', error);
    });

})