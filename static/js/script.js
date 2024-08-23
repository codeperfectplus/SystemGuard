$(document).ready(function() {
    // Any custom JS animations or functionalities can go here.
});
document.addEventListener('DOMContentLoaded', function () {
    const batteryCard = document.querySelector('.battery-card');
    const batteryPercent = parseInt(batteryCard.getAttribute('data-battery'), 10);

    let backgroundColor;

    if (batteryPercent >= 75) {
        backgroundColor = 'linear-gradient(135deg, #76c7c0, #4caf50)';  // Green
    } else if (batteryPercent >= 50) {
        backgroundColor = 'linear-gradient(135deg, #fbc02d, #ffeb3b)';  // Yellow
    } else if (batteryPercent >= 25) {
        backgroundColor = 'linear-gradient(135deg, #ff7043, #ff9800)';  // Orange
    } else {
        backgroundColor = 'linear-gradient(135deg, #f44336, #d32f2f)';  // Red
    }

    batteryCard.style.background = backgroundColor;
});
