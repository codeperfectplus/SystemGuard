// Get CPU and time data from Jinja
console.log("Time Data:", {{ time | tojson | safe }});
const cpuData = {{ cpu | tojson }};
const timeData = {{ time | tojson | safe }};

// Create the chart
const ctx = document.getElementById('cpuTimeChart').getContext('2d');
const cpuTimeChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: timeData,  // Use formatted time for labels
        datasets: [{
            label: 'CPU Usage (%)',
            data: cpuData,
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            fill: true,
            tension: 0.4
        }]
    },
    options: {
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Time'
                }
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'CPU Usage (%)'
                }
            }
        }
    }
});

let refreshInterval = {{ user_dashboard_settings.refresh_interval * 1000 }};
let refreshTimeout;

function startRefresh() {
    refreshTimeout = setTimeout(function () {
        location.reload();
    }, refreshInterval);
}

// Start the refresh process
startRefresh();

// Event listener for select input change
document.getElementById('refresh-interval').addEventListener('change', function () {
    // Clear the existing timeout
    clearTimeout(refreshTimeout);

    // Update the interval based on the selected value
    refreshInterval = parseInt(this.value) * 1000;

    // Restart the refresh process with the new interval
    startRefresh();

    // Send the updated refresh interval to the server
    fetch('/update-refresh-interval', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ refresh_interval: parseInt(this.value) })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Refresh interval updated successfully:', data.refresh_interval);
            } else {
                console.error('Failed to update refresh interval:', data.error);
            }
        })
        .catch(error => console.error('Error:', error));
});
