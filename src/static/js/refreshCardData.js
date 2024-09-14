let refreshInterval = 0; // Initialize with a default value
let refreshTimer; // Variable to hold the setInterval timer
let refreshTimeout; // Variable to hold the setTimeout timer

function fetchRefreshInterval() {
    fetch('/api/v1/refresh-interval')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                refreshInterval = data.refresh_interval * 1000; // Convert to milliseconds
                console.log('Refresh interval fetched successfully:', data.refresh_interval);
                startRefresh(); // Start refreshing after fetching the interval
            } else {
                console.error('Failed to fetch refresh interval:', data.error);
            }
        })
        .catch(error => console.error('Error:', error));
}

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

// Function to fetch system data from the API once
function fetchSystemData(apiEndpoint) {
    if (!apiEndpoint) {
        console.error('Missing required parameter: apiEndpoint.');
        return;
    }

    return fetch(apiEndpoint)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log(`Fetched data from ${apiEndpoint}:`, data);
            return data;
        })
        .catch(error => {
            console.error(`Error fetching data from ${apiEndpoint}:`, error);
            return null;  // Return null on error so we can handle it later
        });
}

// Function to update individual cards with the fetched data
function updateCard(cardSelector, dataKey, data, unit = '') {
    const cardElement = document.querySelector(cardSelector);
    if (!cardElement) {
        return;  // Exit early if the card element is not found
    }

    const dataValue = data[dataKey];
    if (dataValue === undefined) {
        console.warn(`Data key ${dataKey} not found in the response.`);
        cardElement.querySelector('.card-text').textContent = 'Data not available';
        return;
    }
    else if (dataValue === null) {
        console.warn(`Data key ${dataKey} is null in the response.`);
        cardElement.querySelector('.card-text').textContent = 'Data not available';
        return;
    }

    cardElement.querySelector('.card-text').textContent = `${dataValue}${unit}`;
}

// Main function to refresh data and update all necessary cards
function refreshData() {
    fetchSystemData('api/system-info').then(data => {
        if (!data) {
            return;  // Don't update cards if the fetch failed
        }
        updateCard('.bg-disk', 'disk_percent', data);         // Disk Usage
        updateCard('.cpu-temp-card', 'current_temp', data, ' °C');  // CPU Temperature
        updateCard('.bg-dashboard-memory', 'dashboard_memory_usage', data);  // Memory Usage
        updateCard('.bg-memory', 'memory_percent', data, '%');  // Memory Usage
        updateCard('.cpu-frequency', 'cpu_frequency', data, " MHz");  // CPU Frequency
        updateCard('.cpu-card-usage', 'cpu_percent', data, '%');   // CPU Usage
        updateCard('.network-received', 'network_received', data, "MB");  // Network Received
        updateCard('.network-sent', 'network_sent', data, "MB");  // Network Sent
        updateCard('.network-stats', 'network_stats', data, "MB");  // Network Sent
        updateCard('.battery-card', 'battery_percent', data, "%");  // Battery
        updateCard('.network-sent', 'network_sent', data, "MB");  // Network Sent
        updateCard('.network-received', 'network_received', data, "MB");  // Network Received
    });
}

// Function to start refreshing data at the set interval
function startRefresh() {
    if (refreshTimer) {
        clearInterval(refreshTimer); // Clear any existing interval
    }
    if (refreshInterval > 0) {
        refreshTimer = setInterval(refreshData, refreshInterval); // Set a new interval
    }
}

console.log('Starting data refresh process...');

// Fetch the refresh interval initially
fetchRefreshInterval();
