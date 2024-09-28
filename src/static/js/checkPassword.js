document.getElementById('password').addEventListener('input', function() {
    let strengthMeter = document.getElementById('password-strength');
    let password = this.value;
    if (password.length >= 8) {
        strengthMeter.textContent = 'Strong';
        strengthMeter.style.color = 'green';
    } else if (password.length >= 4) {
        strengthMeter.textContent = 'Moderate';
        strengthMeter.style.color = 'orange';
    } else {
        strengthMeter.textContent = 'Weak';
        strengthMeter.style.color = 'red';
    }
});

document.getElementById('confirm_password').addEventListener('input', function() {
    let matchStatus = document.getElementById('password-match');
    if (this.value === document.getElementById('password').value) {
        matchStatus.textContent = 'Passwords match';
        matchStatus.style.color = 'green';
    } else {
        matchStatus.textContent = 'Passwords do not match';
        matchStatus.style.color = 'red';
    }
});
