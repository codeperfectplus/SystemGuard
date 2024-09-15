// battery bar color
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

// cpu temp bar color 
document.addEventListener('DOMContentLoaded', function () {
    const tempBar = document.querySelector('.temp-bar');
    const tempPercentage = parseInt(document.querySelector('.cpu-temp-card').getAttribute('data-cpu-temp'), 10);
    
    if (tempPercentage <= 80) {
        tempBar.classList.add('low');
    }
    else if (tempPercentage > 80 && tempPercentage <= 90) {
        tempBar.classList.add('medium');
    }
    else {
        tempBar.classList.add('high');
    }
});

// disk usage-bar  data-disk-usage
document.addEventListener('DOMContentLoaded', function () {
    const diskBar = document.querySelector('.disk-bar');
    const diskPercentage = parseInt(document.querySelector('.disk-usage-card').getAttribute('data-disk-usage'), 10);

    if (diskPercentage <= 50) {
        diskBar.classList.add('low');
    } else if (diskPercentage > 50 && diskPercentage <= 80) {
        diskBar.classList.add('medium');
    } else {
        diskBar.classList.add('high');
    }
});

// cpu-usage-bar
document.addEventListener('DOMContentLoaded', function () {
    const cpuBar = document.querySelector('.cpu-usage-bar');
    const cpuPercentage = parseInt(document.querySelector('.cpu-usage-card').getAttribute('data-cpu-usage'), 10);

    if (cpuPercentage <= 50) {
        cpuBar.classList.add('low');
    } else if (cpuPercentage > 50 && cpuPercentage <= 80) {
        cpuBar.classList.add('medium');
    } else {
        cpuBar.classList.add('high');
    }
});


// memory-usage-bar | data-memory-usage
document.addEventListener('DOMContentLoaded', function () {
    const memoryBar = document.querySelector('.memory-usage-bar');
    const memoryPercentage = parseInt(document.querySelector('.memory-usage-card').getAttribute('data-memory-usage'), 10);
    console.log("memoryBar", memoryBar);
    console.log("memoryPercentage: ", memoryPercentage);
    if (memoryPercentage <= 50) {
        memoryBar.classList.add('low');
    } else if (memoryPercentage > 50 && memoryPercentage <= 80) {
        memoryBar.classList.add('medium');
    } else {
        memoryBar.classList.add('high');
    }
});
