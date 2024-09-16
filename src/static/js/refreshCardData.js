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
// Note: depcrecated in favor of fetchSystemDataWithRetries

// async function fetchSystemData(apiEndpoint) {
//     try {
//         const response = await fetch(apiEndpoint);
//         return await response.json();
//     } catch (error) {
//         console.error(`Error fetching ${apiEndpoint}:`, error);
//         return null;
//     }
// }

async function fetchSystemDataWithRetries(apiEndpoint, retries = 3, delay = 2000) {
    for (let i = 0; i < retries; i++) {
        try {
            const response = await fetch(apiEndpoint);
            if (response.ok) {
                return await response.json();
            } else {
                const errorText = await response.text();
                console.error(`Error fetching ${apiEndpoint} - Status: ${response.status}, Response: ${errorText}`);
            }
        } catch (error) {
            console.error(`Fetch attempt ${i + 1} failed: ${error.message}`);
        }
        if (i < retries - 1) {
            await new Promise(res => setTimeout(res, delay));
        }
    }
    return null; // Return null after exhausting retries
}


let requestQueue = [];
let isRequestInProgress = false;

async function processQueue() {
    if (isRequestInProgress || requestQueue.length === 0) return;
    isRequestInProgress = true;

    const { apiEndpoint, resolve, reject } = requestQueue.shift();
    try {
        const data = await fetchSystemDataWithRetries(apiEndpoint);
        resolve(data);
    } catch (error) {
        reject(error);
    }

    isRequestInProgress = false;
    processQueue(); // Continue processing the next request
}

function queueRequest(apiEndpoint) {
    return new Promise((resolve, reject) => {
        requestQueue.push({ apiEndpoint, resolve, reject });
        processQueue(); // Start processing if not already in progress
    });
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

        // check if maxDataKey is provided
        if (maxDataKey) {
            let maxDataValue = data?.[maxDataKey];
            percentage = dataValue / maxDataValue * 100;
        } else {
            percentage = Math.min(percentage, 100);
        }

        // Set the bar width based on the percentage
        barElement.style.width = `${percentage}%`;
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

async function updateBatteryIcon(iconSelector, batteryStatusKey, batteryPercentKey, data) {
    let iconElement = document.querySelector(iconSelector);
    let batteryStatus = data[batteryStatusKey];
    let batteryPercent = data[batteryPercentKey];

    if (!iconElement) return;
    iconElement.className = '';
    // based on battery status(Charging/Discharging) and percentage, update the icon, to full, half or empty and color
    if (batteryPercent > 50) {
        iconElement.classList.add('battery-icon', 'fas', 'fa-battery-full', batteryStatus === 'Charging' ? 'text-success' : 'text-danger');
    }
    else if (batteryPercent > 25) {
        iconElement.classList.add('battery-icon', 'fas', 'fa-battery-half', batteryStatus === 'Charging' ? 'text-success' : 'text-danger');
    }
    else {
        iconElement.classList.add('battery-icon', 'fas', 'fa-battery-empty', batteryStatus === 'Charging' ? 'text-success' : 'text-danger');
    }
    
}

// Refresh all card data
async function refreshData() {
    const data = await queueRequest('/api/system-info');
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
    updateBatteryIcon('.battery-icon', 'battery_status', 'battery_percent', data); // battery charging status
    updateColorBars(); // Update color bars based on the fetched data
}

// Update the color of bars based on their percentage
function updateColorBars() {
    const barConfigs = [
        { selector: '.battery-bar', dataAttr: 'data-battery', limits: [25, 75] }, // alreday in %
        { selector: '.disk-bar', dataAttr: 'data-disk-usage', limits: [60, 80] }, // alreday in %
        { selector: '.cpu-usage-bar', dataAttr: 'data-cpu-usage', limits: [60, 90] }, // alreday in %
        { selector: '.memory-usage-bar', dataAttr: 'data-memory-usage', limits: [60, 90] },
        { selector: '.frequency-bar', dataAttr: 'data-cpu-frequency', limits: [60, 90] },
        { selector: '.temp-bar', dataAttr: 'data-cpu-temp', limits: [70, 90] }
    ];

    barConfigs.forEach(({ selector, dataAttr, limits }) => {
        const bar = document.querySelector(selector);
        const card = document.querySelector(`[${dataAttr}]`);

        if (!bar || !card) return;
        let card_value = parseFloat(bar.style.width);
        if (isNaN(card_value)) return;

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
