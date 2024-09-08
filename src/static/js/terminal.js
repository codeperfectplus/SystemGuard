document.getElementById('terminal-form').addEventListener('submit', function (event) {
    event.preventDefault();
    let command = document.getElementById('command').value;
    if (command.trim() !== '') {
        let terminal = document.getElementById('terminal');
        terminal.innerHTML += `<span>$ ${command}</span><br>`;
        document.getElementById('command').value = '';

        fetch('/terminal', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `command=${command}`
        })
            .then(response => response.json())
            .then(data => {
                terminal.innerHTML += `<pre>${data.output}</pre><br>`;
                terminal.scrollTop = terminal.scrollHeight;
            });
    }
});