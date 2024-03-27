const dataForm = document.getElementById('dataForm');

dataForm.addEventListener('submit', function(event) {
  event.preventDefault();
  const ticketType = document.getElementById('ticketType').value;
  const isChecked = document.querySelector('input[name="isChecked"]:checked').value;
  const data = { TicketType: ticketType, fullName: fullName, Email: email, Phone: phone, isChecked: isChecked === 'true' };

  localStorage.setItem('data', JSON.stringify(data));
  window.location.href = 'index.html';
});