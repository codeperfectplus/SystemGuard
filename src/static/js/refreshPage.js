let refreshInterval = 0; // Initialize with a default value
let refreshTimeout;

function fetchRefreshInterval() {
    fetch('/api/v1/refresh-interval')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                refreshInterval = data.refresh_interval * 1000; // Multiply by 1000 to convert to milliseconds
                console.log('Refresh interval fetched successfully:', data.refresh_interval);
                startRefresh(); // Start refreshing after fetching the interval
            } else {
                console.error('Failed to fetch refresh interval:', data.error);
            }
        })
        .catch(error => console.error('Error:', error));
}

function startRefresh() {
    if (refreshInterval > 0) { // Only refresh if the interval is greater than 0
        refreshTimeout = setTimeout(function () {
            location.reload();
        }, refreshInterval);
    }
}

// Start the process by fetching the refresh interval
fetchRefreshInterval();

// Event listener for select input change
document.getElementById('refresh-interval').addEventListener('change', function () {
    // Clear the existing timeout
    clearTimeout(refreshTimeout);

    // Update the interval based on the selected value
    refreshInterval = parseInt(this.value) * 1000;  // Convert to milliseconds

    // Restart the refresh process if a valid interval is selected
    startRefresh();

    // Send the updated refresh interval to the server
    fetch('/api/v1/refresh-interval', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ refresh_interval: parseInt(this.value) })  // Send in seconds, not milliseconds
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
