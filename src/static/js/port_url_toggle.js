function toggleFields() {
    var selection = document.getElementById('type_selection').value;
    var ipField = document.getElementById('ip_address');
    var portField = document.getElementById('port');
    var linkField = document.getElementById('link');

    if (selection === 'link') {
        ipField.disabled = true;
        portField.disabled = true;
        linkField.disabled = false;
        document.getElementById('ip_group').style.display = 'none';
        document.getElementById('port_group').style.display = 'none';
        document.getElementById('link_group').style.display = 'block';
    } else {
        ipField.disabled = false;
        portField.disabled = false;
        linkField.disabled = true;
        document.getElementById('ip_group').style.display = 'block';
        document.getElementById('port_group').style.display = 'block';
        document.getElementById('link_group').style.display = 'none';
    }
}

window.onload = function () {
    toggleFields(); // Initialize the fields based on the current selection
};