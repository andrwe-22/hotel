/// admin_page.js ///


document.addEventListener("DOMContentLoaded", function() {
    var ctx = document.getElementById('bookingChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: roomNumbers,
            datasets: [{
                label: 'Booking Count',
                data: bookingCounts,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
