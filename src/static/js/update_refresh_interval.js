// let refreshInterval = {{ user_dashboard_settings.refresh_interval * 1000 }}; // Multiply by 1000 initially

// Fetch the refresh interval from the server
fetch('/get-refresh-interval')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            refreshInterval = data.refresh_interval * 1000; // Multiply by 1000 to convert to milliseconds
            console.log('Refresh interval fetched successfully:', refreshInterval);
        } else {
            console.error('Failed to fetch refresh interval:', data.error);
        }
    })
    .catch(error => console.error('Error:', error));
    
let refreshTimeout;

// Event listener for select input change
document.getElementById('refresh-interval').addEventListener('change', function () {
    // Clear the existing timeout
    clearTimeout(refreshTimeout);

    // Update the interval based on the selected value
    refreshInterval = parseInt(this.value) * 1000;  // Convert to milliseconds

    // refresh the page once
    refreshTimeout = setTimeout(() => {
        window.location.reload();
    }, refreshInterval);

    // Send the updated refresh interval to the server
    fetch('/update-refresh-interval', {
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
