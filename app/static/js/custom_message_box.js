function showMessage(type, message, messageId, waitTime) {
    const messageBox = document.getElementById(messageId);
    messageBox.textContent = message;
    messageBox.className = 'message-box';

    if (type === 'success') {
        messageBox.classList.add('success');
    } else if (type === 'error') {
        messageBox.classList.add('error');
    } else if (type === "info") {
        messageBox.classList.add('info');
    }

    messageBox.style.display = 'block';
    setTimeout(function () {
        messageBox.style.display = 'none';
    }, waitTime);
}
