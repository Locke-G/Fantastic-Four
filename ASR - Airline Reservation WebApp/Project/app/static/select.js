const seats = document.querySelectorAll('.seat');
const selectedSeat = document.getElementById('selectedSeat');

document.addEventListener("DOMContentLoaded", function() {
    seats.forEach(seat => {
    seat.addEventListener('click', event => {
        seats.forEach(seat => seat.classList.remove('selected'));
        event.target.classList.add('selected');
        selectedSeat.value = event.target.id;
    });
});
});
