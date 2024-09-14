document.addEventListener('DOMContentLoaded', function () {
    const batteryBar = document.querySelector('.battery-bar');
    const batteryPercentage = parseInt(document.querySelector('.battery-card').getAttribute('data-battery'), 10);

    if (batteryPercentage <= 25) {
        batteryBar.classList.add('low');
    } else if (batteryPercentage > 25 && batteryPercentage <= 75) {
        batteryBar.classList.add('medium');
    } else {
        batteryBar.classList.add('high');
    }
});