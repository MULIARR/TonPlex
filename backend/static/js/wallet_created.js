const tg = window.Telegram.WebApp;
tg.expand();

tg.MainButton.text = "Skip And Continue";

tg.MainButton.onClick(function() {
    openWallet();
});

tg.MainButton.show();

function copyToClipboard() {
    const button = document.querySelector('.copy-button');
    const textToCopy = button.getAttribute('data-phrase');

    navigator.clipboard.writeText(textToCopy)
        .then(() => {
            button.innerText = 'Copied';
            button.style.border = '2px solid seagreen';
            tg.MainButton.text = "Let's Start!";
        })
        .catch(err => {
            console.error('Could not copy seed-phrase: ', err);
        });
}

function openWallet() {
    const userId = tg.initDataUnsafe.user.id
    window.location.href = `/wallet?user_id=${userId}`;
}