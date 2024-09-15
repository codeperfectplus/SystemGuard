// Function to format time in HH:MM:SS
function formatTime(hours, minutes, seconds) {
    let date = new Date();
    let day = date.getDate().toString().padStart(2, '0');
    let month = (date.getMonth() + 1).toString().padStart(2, '0');
    let year = date.getFullYear().toString();
    let formattedDate = year + '-' + month + '-' + day;
    let formattedTime = hours.toString().padStart(2, '0') + ':' + minutes.toString().padStart(2, '0') + ':' + seconds.toString().padStart(2, '0');
    return `${formattedDate} ${formattedTime}`;
}

// Initialize the time from the server
let timeElement = document.getElementById('server-time');
if (timeElement) {
    let serverTime = new Date(timeElement.textContent);

    // Update the time every second
    setInterval(() => {
        // Increment the server time by 1 second
        serverTime.setSeconds(serverTime.getSeconds() + 1);
        // Update the displayed time
        timeElement.textContent = formatTime(
            serverTime.getHours(),
            serverTime.getMinutes(),
            serverTime.getSeconds()
        );
    }, 1000);
};
// code to update the system uptime
let bootTimeElement = document.getElementById('system-uptime');
if (bootTimeElement) {
    let bootTime = bootTimeElement.textContent;

    // Function to format uptime as 'X days, Y hours, Z minutes, W seconds'
    function formatUptime(days, hours, minutes, seconds) {
        let uptimeString = '';
        if (days > 0) {
            uptimeString += `${days} days, `;
        }
        if (hours > 0 || days > 0) { // Show hours if days > 0 even if hours is 0
            uptimeString += `${hours} hours, `;
        }
        uptimeString += `${minutes} minutes, ${seconds} seconds`;
        return uptimeString;
    }

    let bootTimeArray = bootTime.split(', ');
    let days = parseInt(bootTimeArray[0].trim().split(' ')[0]);
    let hours = parseInt(bootTimeArray[1].trim().split(' ')[0]);
    let minutes = parseInt(bootTimeArray[2].trim().split(' ')[0]);
    let seconds = parseInt(bootTimeArray[3].trim().split(' ')[0]);

    // Function to update uptime
    function updateUptime() {
        seconds++;
        if (seconds >= 60) {
            seconds = 0;
            minutes++;
            if (minutes >= 60) {
                minutes = 0;
                hours++;
                if (hours >= 24) {
                    hours = 0;
                    days++;
                }
            }
        }

        // Update the display
        bootTimeElement.textContent = formatUptime(days, hours, minutes, seconds);
    }

    // Update the uptime every second
    setInterval(updateUptime, 1000);
};
