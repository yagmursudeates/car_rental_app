document.addEventListener('DOMContentLoaded', () => {
    console.log("Scripts loaded!");

    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 1000);
        }, 3000);
    });
});
