setTimeout(function () {
    const alert = document.querySelector('.alert-dismissible');
    if (alert) {
        const alertInstance = bootstrap.Alert.getOrCreateInstance(alert);
        alertInstance.close();
    }
}, 5000);

