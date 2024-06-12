const tg = window.Telegram.WebApp;
const userId = tg.initDataUnsafe.user.id;

window.location.href = `/redirect?user_id=${userId}`;