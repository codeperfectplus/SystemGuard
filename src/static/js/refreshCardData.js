let refreshInterval = 0;
let refreshTimer, refreshTimeout;

// Fetch the refresh interval from the server
async function fetchRefreshInterval() {
    try {
        const response = await fetch('/api/v1/refresh-interval');
        const data = await response.json();
        if (data.success) {
            refreshInterval = data.refresh_interval * 1000; // Convert to ms
            return refreshInterval;
        } else {
            console.error('Error fetching interval:', data.error);
        }
    } catch (error) {
        console.error('Fetch interval error:', error);
    }
}

// Update the refresh interval when the user changes the value
function updateRefreshInterval() {
    const refreshInput = document.getElementById('refresh-interval');
    refreshInput.addEventListener('change', function () {
        clearTimeout(refreshTimeout);
        refreshInterval = parseInt(this.value) * 1000;
        refreshTimeout = setTimeout(() => window.location.reload(), refreshInterval);
        postRefreshInterval(refreshInterval / 1000); // Send in seconds
    });
}

// Post the updated refresh interval to the server
async function postRefreshInterval(newInterval) {
    try {
        const response = await fetch('/api/v1/refresh-interval', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh_interval: newInterval })
        });
        const data = await response.json();
        if (data.success) {
            console.log('Updated interval:', data.refresh_interval);
        } else {
            console.error('Failed to update interval:', data.error);
        }
    } catch (error) {
        console.error('Error updating interval:', error);
    }
}

// Fetch system data from a given API endpoint
async function fetchSystemData(apiEndpoint) {
    try {
        const response = await fetch(apiEndpoint);
        return await response.json();
    } catch (error) {
        console.error(`Error fetching ${apiEndpoint}:`, error);
        return null;
    }
}

// Update card content and bar width based on fetched data
function updateCard(cardSelector, dataKey, data, unit = '', barSelector = null) {
    const cardElement = document.querySelector(cardSelector);
    if (!cardElement) return;

    const dataValue = data?.[dataKey];
    cardElement.querySelector('.card-text').textContent = dataValue ? `${dataValue}${unit}` : 'Data not available';

    // Update the bar width if a bar selector is provided
    if (barSelector) {
        const barElement = cardElement.querySelector(barSelector);
        if (!barElement) return;

        const percentage = parseFloat(dataValue);
        if (!isNaN(percentage)) {
            barElement.style.width = `${percentage}%`;
        }
    }
}

// Refresh all card data
async function refreshData() {
    const data = await fetchSystemData('/api/system-info');
    if (!data) return;

    updateCard('.bg-disk', 'disk_percent', data, '%', '.disk-bar');
    updateCard('.cpu-temp-card', 'current_temp', data, ' °C', '.temp-bar');
    updateCard('.bg-memory', 'memory_percent', data, '%', '.memory-usage-bar');
    updateCard('.cpu-frequency', 'cpu_frequency', data, ' MHz', '.frequency-bar');
    updateCard('.cpu-usage-card', 'cpu_percent', data, '%', '.cpu-usage-bar');
    updateCard('.network-received', 'network_received', data, 'MB');
    updateCard('.network-sent', 'network_sent', data, 'MB');
    updateCard('.battery-card', 'battery_percent', data, '%', '.battery-bar');
    updateColorBars(); // Update color bars based on the fetched data
}

// Update the color of bars based on their percentage
function updateColorBars() {
    const barConfigs = [
        { selector: '.battery-bar', dataAttr: 'data-battery', limits: [25, 75] },
        { selector: '.disk-bar', dataAttr: 'data-disk-usage', limits: [60, 80] },
        { selector: '.cpu-usage-bar', dataAttr: 'data-cpu-usage', limits: [50, 80] },
        { selector: '.memory-usage-bar', dataAttr: 'data-memory-usage', limits: [.50, .80], maxAttr: 'data-memory-total' },
        { selector: '.frequency-bar', dataAttr: 'data-cpu-frequency', limits: [.50, .80], maxAttr: 'data-cpu-max-frequency' },
        { selector: '.temp-bar', dataAttr: 'data-cpu-temp', limits: [.70, .90], maxAttr: 'data-cpu-max-temp' }
    ];

    barConfigs.forEach(({ selector, dataAttr, limits, maxAttr }) => {
        const bar = document.querySelector(selector);
        const card = document.querySelector(`[${dataAttr}]`);
        const maxElement = maxAttr ? document.querySelector(`[${maxAttr}]`) : null;

        if (!bar || !card) return;
        let percentage = parseFloat(bar.style.width);
        if (isNaN(percentage)) return;

        if (maxElement) {
            const maxValue = parseFloat(maxElement.getAttribute(maxAttr));
            if (!isNaN(maxValue)) {
                limits = [maxValue * limits[0], maxValue * limits[1]];
            }
        }

        percentage = Math.min(percentage, 100); // Ensure percentage is not greater than 100
        bar.classList.remove('low', 'medium', 'high');
        // Apply the appropriate class based on the limits
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
async function init() {
    await fetchRefreshInterval();
    startRefresh(); // Start refreshing data at the set interval
    updateRefreshInterval(); // Listen for changes in the refresh interval input
    updateColorBars(); // Update the color bars based on the initial data
}

document.addEventListener('DOMContentLoaded', init);
