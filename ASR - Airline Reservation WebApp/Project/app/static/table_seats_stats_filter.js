function filterSeats() {
    let seats = document.querySelectorAll('.seat');
    let airlineFilter = document.getElementById('airline-filter').value;
    let statusFilter = document.getElementById('status-filter').value;

    seats.forEach(seat => {
        let airline = seat.querySelector('.airline').textContent;
        let status = seat.querySelector('.status').textContent;

        if (
            (airlineFilter === '' || airline === airlineFilter) &&
            (statusFilter === '' || status === statusFilter)
        ) {
            seat.style.display = 'table-row';
        } else {
            seat.style.display = 'none';
        }
    });
}
let filters = document.querySelectorAll('select');
filters.forEach(filter => {
    filter.addEventListener('change', filterSeats);
});