document.getElementById('updateButton').addEventListener('click', function (event) {
    event.preventDefault(); // Prevent the default link behavior

    fetch('{{ url_for("update_git_version") }}', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // Add any additional headers if needed
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Update successful: ' + data.message);
            } else {
                alert('Update failed: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while updating.');
        });
});