let refreshInterval = 0;
let refreshTimer, refreshTimeout;

// Fetch the refresh interval from the server
function fetchRefreshInterval() {
    return fetch('/api/v1/refresh-interval')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                refreshInterval = data.refresh_interval * 1000; // Convert to ms
                console.log('Refresh interval:', data.refresh_interval);
                return refreshInterval;
            } else {
                console.error('Error fetching interval:', data.error);
            }
        })
        .catch(error => console.error('Fetch interval error:', error));
}

// Update the refresh interval when the user changes the value
function updateRefreshInterval() {
    const refreshInput = document.getElementById('refresh-interval');
    refreshInput.addEventListener('change', function () {
        clearTimeout(refreshTimeout);
        refreshInterval = parseInt(this.value) * 1000;

        refreshTimeout = setTimeout(() => window.location.reload(), refreshInterval);
        
        postRefreshInterval(refreshInterval / 1000); // Send in seconds
        updateColorBars(); // Update color bars based on data attributes
});
}

// Post the updated refresh interval to the server
function postRefreshInterval(newInterval) {
    fetch('/api/v1/refresh-interval', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_interval: newInterval })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Updated interval:', data.refresh_interval);
            } else {
                console.error('Failed to update interval:', data.error);
            }
        })
        .catch(error => console.error('Error:', error));
}

// Fetch system data from a given API endpoint
function fetchSystemData(apiEndpoint) {
    return fetch(apiEndpoint)
        .then(response => response.json())
        .catch(error => {
            console.error(`Error fetching ${apiEndpoint}:`, error);
            return null;
        });
}

// Update card content based on the fetched data
function updateCard(cardSelector, dataKey, data, unit = '', barSelector) {
    const cardElement = document.querySelector(cardSelector);
    if (!cardElement) return;
    
    const dataValue = data?.[dataKey];
    cardElement.querySelector('.card-text').textContent = dataValue 
        ? `${dataValue}${unit}` 
        : 'Data not available';

    // update the bar element if a selector is provided
    if (barSelector) {
        const barElement = cardElement.querySelector(barSelector);
        if (!barElement) return;

        // update the bar element based on the data value
        const percentage = parseFloat(dataValue);
        if (isNaN(percentage)) return;

        barElement.style.width = `${percentage}%`;
    }
}


// Refresh all card data
function refreshData() {
    fetchSystemData('/api/system-info').then(data => {
        if (!data) return;
        updateCard('.bg-disk', 'disk_percent', data, '%', '.disk-bar');
        updateCard('.cpu-temp-card', 'current_temp', data, ' °C', '.temp-bar');
        updateCard('.bg-memory', 'memory_percent', data, '%', '.memory-usage-bar');
        updateCard('.cpu-frequency', 'cpu_frequency', data, ' MHz', '.frequency-bar');
        updateCard('.cpu-usage-card', 'cpu_percent', data, '%', '.cpu-usage-bar');
        updateCard('.network-received', 'network_received', data, 'MB');
        updateCard('.network-sent', 'network_sent', data, 'MB');
        updateCard('.battery-card', 'battery_percent', data, '%', '.battery-bar');
        updateColorBars(); // Update color bars based on data attributes
    });
}

// Update color bars based on data attributes
function updateColorBars() {
    const bars = [
        { selector: '.battery-bar', dataAttr: 'data-battery', limits: [25, 75] },
        { selector: '.disk-bar', dataAttr: 'data-disk-usage', limits: [60, 80] },
        { selector: '.cpu-usage-bar', dataAttr: 'data-cpu-usage', limits: [50, 80] },
        { selector: '.memory-usage-bar', dataAttr: 'data-memory-usage', limits: [0.5, 0.8], maxAttr: 'data-memory-total' },
        { selector: '.frequency-bar', dataAttr: 'data-cpu-frequency', limits: [0.5, 0.8], maxAttr: 'data-cpu-max-frequency' },
        { selector: '.temp-bar', dataAttr: 'data-cpu-temp', limits: [0.65, 0.9], maxAttr: 'data-cpu-max-temp' }
    ];

    bars.forEach(({ selector, dataAttr, limits, maxAttr }) => {
        const bar = document.querySelector(selector);
        const card = document.querySelector(`[${dataAttr}]`);
        const maxElement = maxAttr ? document.querySelector(`[${maxAttr}]`) : null;

        if (!bar || !card) {
            // console.warn(`Element not found for selector: ${selector} or data attribute: ${dataAttr}`);
            return;
        }

        let percentage = parseFloat(card.getAttribute(dataAttr));

        if (isNaN(percentage)) {
            console.warn(`Invalid percentage value for ${dataAttr}`);
            return;
        }

        // If maxAttr is defined, use it to scale the limits
        if (maxElement) {
            const maxValue = parseFloat(maxElement.getAttribute(maxAttr));
            if (isNaN(maxValue)) {
                // console.warn(`Invalid max value for ${maxAttr}`);
                return;
            }

            limits = [maxValue * limits[0], maxValue * limits[1]];
        }

        // Apply class based on percentage within the defined limits
        if (percentage <= limits[0]) {
            bar.classList.add('low');
        } else if (percentage > limits[0] && percentage <= limits[1]) {
            bar.classList.add('medium');
        } else {
            bar.classList.add('high');
        }
    });
}


// Start the automatic refresh process
function startRefresh() {
    clearInterval(refreshTimer);
    if (refreshInterval > 0) {
        refreshTimer = setInterval(refreshData, refreshInterval);
    }
}

// Initialize the system
function init() {
    fetchRefreshInterval().then(startRefresh); // Fetch interval and start refreshing
    updateRefreshInterval(); // Listen for changes to the refresh interval input
    updateColorBars(); // Update color bars based on data attributes
}

document.addEventListener('DOMContentLoaded', init);
