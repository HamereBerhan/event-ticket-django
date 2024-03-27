const message = document.getElementById('message');
const form1 = document.getElementById('form1');
const form2 = document.getElementById('form2');
const form3 = document.getElementById('form3');
const form4 = document.getElementById('form4');
const checkInButton = document.getElementById('checkInButton');
const checkInButton2 = document.getElementById('checkInButton2');

const data = JSON.parse(localStorage.getItem('data'));

if (data.isChecked) {
    form3.style.display = 'flex';
} else if (!data.isChecked && data.TicketType === "1") {
    form1.style.display = 'flex';
    document.getElementById('first_name').textContent = data.first_name;
    document.getElementById('last_name').textContent = data.last_name;
    document.getElementById('email').textContent = data.Email;
    document.getElementById('phone').textContent = data.Phone;
    checkInButton.addEventListener('click', function() {
        sendDataToBackend({ checkedin: 1 });
    });
} else if (!data.isChecked && data.TicketType === "2") {
    form2.style.display = 'flex';
    checkInButton2.addEventListener('click', function() {
        const first_name = document.getElementById('first_name').value;
        const phoneNumber = document.getElementById('phoneNumber').value;
        const email = document.getElementById('email').value;
        if (first_name && phoneNumber) {
            email = null;
            sendDataToBackend({ first_name, phoneNumber, email, checkedin: 1 });
        } else {
            alert('Please fill in all fields.');
        }
    });
}

function sendDataToBackend(data) {
    console.log('Data sent to the backend:', data);
}
