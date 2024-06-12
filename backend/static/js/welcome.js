const tg = window.Telegram.WebApp;

document.getElementById('create-wallet').addEventListener('click', function() {
    const userModel = tg.initDataUnsafe.user

    const baseUrl = window.location.origin;
    fetch(`${baseUrl}/api/wallet_setup/create`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userModel)
    })
        .then(response => {
            if (response.ok) {
                window.location.href = response.url;
            } else {
                return response.json().then(data => {
                    console.error('Error:', data);
                });
            }
        })
        .catch(error => console.error('Error:', error));
});

document.getElementById('import-wallet').addEventListener('click', function() {
    window.location.href = '/wallet_setup/import';
});