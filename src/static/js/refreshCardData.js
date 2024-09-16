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
function updateCard(cardSelector, dataKey, data, unit = '', barSelector = null, maxDataKey = null) {
    const cardElement = document.querySelector(cardSelector);
    if (!cardElement) return;

    let dataValue = data?.[dataKey];
    cardElement.querySelector('.card-text').textContent = dataValue ? `${dataValue}${unit}` : 'Data not available';

    // Update the bar width if a bar selector is provided
    if (barSelector) {
        const barElement = cardElement.querySelector(barSelector);
        if (!barElement) return;

        let percentage = parseFloat(dataValue);

        if (!isNaN(percentage)) {
            // If a maxDataKey is provided, calculate the percentage based on the max value
            if (maxDataKey) {
                const maxDataValue = parseFloat(data?.[maxDataKey]);
                if (!isNaN(maxDataValue) && maxDataValue > 0) {
                    percentage = (percentage / maxDataValue) * 100;
                }
            }

            // Ensure the percentage doesn't exceed 100%
            percentage = Math.min(percentage, 100);

            // Set the bar width based on the percentage
            barElement.style.width = `${percentage}%`;
        }
    }
}

// refresh the card text based on fetched data
async function refreshCardText(cardSelector, dataKey, data) {
    const cardElement = document.querySelector(cardSelector);

    if (!cardElement) return;
    // fetch value dataKey from data
    let dataValue = data[dataKey];

    // Update the card text
    if (dataValue) {
        cardElement.textContent = `Battery Status: ${dataValue}`;
    } else {
        cardElement.textContent = 'Data not available';
    }
}

// Refresh all card data
async function refreshData() {
    const data = await fetchSystemData('/api/system-info');
    if (!data) return;

    updateCard('.bg-disk', 'disk_percent', data, '%', '.disk-bar');
    updateCard('.cpu-temp-card', 'current_temp', data, ' °C', '.temp-bar');
    updateCard('.bg-memory', 'memory_percent', data, '%', '.memory-usage-bar');
    updateCard('.cpu-frequency-card', 'cpu_frequency', data, ' MHz', '.frequency-bar', 'cpu_max_frequency');
    updateCard('.cpu-usage-card', 'cpu_percent', data, '%', '.cpu-usage-bar');
    updateCard('.network-received', 'network_received', data, 'MB');
    updateCard('.network-sent', 'network_sent', data, 'MB');
    updateCard('.battery-card', 'battery_percent', data, '%', '.battery-bar');

    refreshCardText('.battery-status', 'battery_status', data); // battery charging status
    updateColorBars(); // Update color bars based on the fetched data
}

// Update the color of bars based on their percentage
function updateColorBars() {
    const barConfigs = [
        { selector: '.battery-bar', dataAttr: 'data-battery', limits: [25, 75] }, // alreday in %
        { selector: '.disk-bar', dataAttr: 'data-disk-usage', limits: [60, 80] }, // alreday in %
        { selector: '.cpu-usage-bar', dataAttr: 'data-cpu-usage', limits: [60, 90] }, // alreday in %
        { selector: '.memory-usage-bar', dataAttr: 'data-memory-usage', limits: [60, 90], maxAttr: 'data-memory-total' },
        { selector: '.frequency-bar', dataAttr: 'data-cpu-frequency', limits: [60, 90], maxAttr: 'data-cpu-max-frequency' },
        { selector: '.temp-bar', dataAttr: 'data-cpu-temp', limits: [70, 90], maxAttr: 'data-cpu-max-temp' }
    ];

    barConfigs.forEach(({ selector, dataAttr, limits, maxAttr }) => {
        const bar = document.querySelector(selector);
        const card = document.querySelector(`[${dataAttr}]`);
        const maxElement = maxAttr ? document.querySelector(`[${maxAttr}]`) : null;

        if (!bar || !card) return;
        let card_value = parseFloat(bar.style.width);
        if (isNaN(card_value)) return;

        if (maxElement) {
            const maxValue = parseFloat(maxElement.getAttribute(maxAttr));
            if (!isNaN(maxValue)) {
                limits = [maxValue * limits[0]/100, maxValue * limits[1]/100];
            }
        }
        // console.log("card_value", card_value, limits)
        bar.classList.remove('low', 'medium', 'high');
        // Apply the appropriate class based on the limits
        if (card_value <= limits[0]) {
            bar.classList.add('low');
        } else if (card_value > limits[0] && card_value <= limits[1]) {
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
