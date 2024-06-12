document.addEventListener('DOMContentLoaded', function() {
    const tg = window.Telegram.WebApp;

    const elements = document.querySelectorAll('.diff_24h');

    const sendForm = document.getElementById('send-form');
    const inputs = sendForm.querySelectorAll('input');
    const indentForKeyboard = document.querySelector('.indent-for-keyboard');

    const bottomSheetSend = document.getElementById('bottom-sheet-send');
    const transactionStatus = document.getElementById('transaction-status');
    const transactionStatusMessage = document.getElementById('transaction-status-message');
    const overlay = document.getElementById('overlay');
    const closeBtns = document.querySelectorAll('.close');

    const openBtnTransactions = document.getElementById('open-bottom-sheet-transactions');
    const openBtnReceive = document.getElementById('open-bottom-sheet-receive');
    const openBtnSend = document.getElementById('open-bottom-sheet-send');
    const openBtnSeedPhrase = document.getElementById('open-bottom-sheet-seed-phrase');

    const bottomSheetReceive = document.getElementById('bottom-sheet-receive');
    const bottomSheetSeedPhrase = document.getElementById('bottom-sheet-seed-phrase');

    const bottomSheetTransactions = document.getElementById('bottom-sheet-transactions');


    function updateColors() {
        elements.forEach(function(element) {
            const text = element.textContent.trim();

            if (text.startsWith('+')) {
                element.style.color = 'seagreen';
            } else {
                element.style.color = '#dc3545';
            }
        });
    }

    updateColors();


    let startY = 0;
    let isPulling = false;

    window.addEventListener('touchstart', function(event) {
        if (window.scrollY === 0) {
            startY = event.touches[0].pageY;
            isPulling = true;
        }
    });

    window.addEventListener('touchmove', function(event) {
        if (isPulling) {
            const currentY = event.touches[0].pageY;
            if (currentY - startY > 65) {
                location.reload();
                isPulling = false;
            }
        }
    });

    window.addEventListener('touchend', function() {
        isPulling = false;
    });


    const isMobile = tg.platform === 'mobile' || window.innerWidth < 600;

    if (isMobile) {
        indentForKeyboard.style.paddingBottom = '40vh';
    }

    function closeModal(modal) {
        modal.classList.add('hide');
        setTimeout(() => {
            modal.classList.remove('show');
            modal.classList.remove('hide');
            overlay.style.display = 'none';
        }, 500);
    }

    openBtnReceive.addEventListener('click', function() {
        bottomSheetReceive.classList.add('show');
        overlay.style.display = 'block';
    });

    openBtnSend.addEventListener('click', function() {
        bottomSheetSend.classList.add('show');
        overlay.style.display = 'block';
    });

    openBtnSeedPhrase.addEventListener('click', function() {
        bottomSheetSeedPhrase.classList.add('show');
        overlay.style.display = 'block';
    });

    openBtnTransactions.addEventListener('click', function() {
        bottomSheetTransactions.classList.add('show');
        overlay.style.display = 'block';
    });

    closeBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            if (btn.closest('.bottom-sheet')) {
                closeModal(btn.closest('.bottom-sheet'));
            }
        });
    });

    window.addEventListener('click', function(event) {
        if (event.target === overlay) {
            closeModal(bottomSheetReceive);
            closeModal(bottomSheetSend);
            closeModal(bottomSheetSeedPhrase);
            closeModal(transactionStatus);
            closeModal(bottomSheetTransactions);
        }
    });

    function clearBorders() {
        inputs.forEach(input => {
            input.style.border = '2px solid transparent';
        });
    }


    sendForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const amount = parseFloat(sendForm.elements['amount'].value);
        const address = sendForm.elements['address'].value.trim();
        const memo = sendForm.elements['memo'].value.trim();

        let isValid = true;
        if (isNaN(amount) || amount <= 0) {
            sendForm.elements['amount'].style.border = '2px solid #dc3545';
            isValid = false;
        } else {
            sendForm.elements['amount'].style.border = '2px solid seagreen';
        }
        if (address.length <= 20 || /\s/.test(address)) {
            sendForm.elements['address'].style.border = '2px solid #dc3545';
            isValid = false;
        } else {
            sendForm.elements['address'].style.border = '2px solid seagreen';
        }

        if (!isValid) {
            return;
        }

        closeModal(bottomSheetSend);

        sendForm.reset();
        clearBorders();

        const transactionModel = {
            'user_id': 6645125297, // tg.initDataUnsafe.user.id,
            'amount': amount,
            'to_address': address,
            'memo': memo
        }

        transactionStatusMessage.innerText = 'Processing...';
        transactionStatus.classList.add('show');
        overlay.style.display = 'block';

        const baseUrl = window.location.origin;
        fetch(`${baseUrl}/api/wallet/send_transaction`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(transactionModel)
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    transactionStatusMessage.innerText = 'Toncoin sent successfully!';
                } else {
                    transactionStatusMessage.innerText = 'Sending error.';
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });

    });
});

function copyToClipboardSeedPhrase() {
    const button = document.querySelector('.copy-seed-phrase-button');
    const textToCopy = button.getAttribute('data-phrase');

    navigator.clipboard.writeText(textToCopy)
        .then(() => {
            button.innerText = 'Copied';
            button.style.border = '2px solid seagreen';
        })
        .catch(err => {
            console.error('Could not copy seed-phrase: ', err);
        });
}

function copyToClipboardAddress() {
    const button = document.querySelector('.copy-address-button');
    const addressToCopy = button.getAttribute('data-address');

    navigator.clipboard.writeText(addressToCopy)
        .then(() => {
            button.innerText = 'Copied';
            button.style.border = '2px solid seagreen';
        })
        .catch(err => {
            console.error('Could not copy seed-phrase: ', err);
        });
}