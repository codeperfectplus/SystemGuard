$(document).ready(function() {
    // Any custom JS animations or functionalities can go here.
});

// Function to get gradient color based on value ranges
function getGradientColor(value, thresholds, isReversed = false) {
    // If reversed, swap the color logic
    if (isReversed) {
        if (value >= thresholds.high) {
            return 'linear-gradient(135deg, #ff0000, #ff8a80)';  // Red (high value is bad)
        } else if (value >= thresholds.mediumHigh) {
            return 'linear-gradient(135deg, #ff9800, #ffcc80)';  // Orange
        } else if (value >= thresholds.mediumLow) {
            return 'linear-gradient(135deg, #ffeb3b, #fdd835)';  // Yellow
        } else {
            return 'linear-gradient(135deg, #4caf50, #a5d6a7)';  // Green (low value is good)
        }
    } else {
        // Normal logic (e.g., for battery where high value is good)
        if (value >= thresholds.high) {
            return 'linear-gradient(135deg, #4caf50, #a5d6a7)';  // Green (high value is good)
        } else if (value >= thresholds.mediumHigh) {
            return 'linear-gradient(135deg, #ffeb3b, #fdd835)';  // Yellow
        } else if (value >= thresholds.mediumLow) {
            return 'linear-gradient(135deg, #ff9800, #ffcc80)';  // Orange
        } else {
            return 'linear-gradient(135deg, #ff0000, #ff8a80)';  // Red (low value is bad)
        }
    }
}

// Function to apply gradient color for CPU usage and temperature (reversed logic for CPU)
function applyGradient(element, value, thresholds, isReversed = false) {
    const backgroundColor = getGradientColor(value, thresholds, isReversed);
    element.style.background = backgroundColor;
}

document.addEventListener('DOMContentLoaded', function () {
    // Battery Card (High percentage is good)
    const batteryCard = document.querySelector('.battery-card');
    const batteryPercent = parseInt(batteryCard.getAttribute('data-battery'), 10);
    applyGradient(batteryCard, batteryPercent, {
        high: 75,
        mediumHigh: 50,
        mediumLow: 25
    }, false);  // `false` for normal logic (high percentage is good)

    // CPU Usage Card (Low usage percentage is good)
    // const cpuUsageCard = document.querySelector('.cpu-usage-card');
    // const cpuUsagePercent = parseInt(cpuUsageCard.getAttribute('data-cpu-usage'), 10);
    // applyGradient(cpuUsageCard, cpuUsagePercent, {
    //     high: 90,
    //     mediumHigh: 70,
    //     mediumLow: 60
    // }, true);  // `true` to reverse logic (low percentage is good)

    // CPU Temperature Card (Low temperature is good)
    const cpuTemperatureCard = document.querySelector('.cpu-temp-card');
    const cpuTemperature = parseInt(cpuTemperatureCard.getAttribute('data-cpu-temp'), 10);
    // TODO: take max temperature from the system and set it as the high value
    applyGradient(cpuTemperatureCard, cpuTemperature, {
        high: 90,
        mediumHigh: 70,
        mediumLow: 60
    }, true);  // `true` to reverse logic (low temperature is good)
});
