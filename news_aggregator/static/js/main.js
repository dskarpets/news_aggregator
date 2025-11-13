function toggleSettings() {
    const panel = document.getElementById('settingsPanel');
    panel.classList.toggle('active');
}

document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.animation = 'slideOut 0.3s';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
});
