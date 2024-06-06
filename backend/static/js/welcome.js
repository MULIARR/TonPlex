document.getElementById('create-wallet').addEventListener('click', function() {
    fetch('/api/import_wallet', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: 'example_user_id' })
    })
});