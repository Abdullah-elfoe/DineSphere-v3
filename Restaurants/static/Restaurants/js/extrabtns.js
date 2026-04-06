// -------------------------------
// GET SELECTED CARD
// -------------------------------
function getSelectedCard() {
    return document.querySelector('.clickable-card.selected');
}


// -------------------------------
// CSRF TOKEN
// -------------------------------
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}


// -------------------------------
// GENERIC POST
// -------------------------------
function sendPost(url, payload) {
    return fetch(url, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams(payload)
    })
    .then(res => {
        if (!res.ok) throw new Error("Request failed");
        return res.text();
    });
}


// -------------------------------
// BOOKING → FINISH
// -------------------------------
document.querySelector('.booking_finish')?.addEventListener('click', () => {
    const card = getSelectedCard();
    if (!card) return alert("Select a booking first!");

    const id = card.dataset.id;

    sendPost('/business/markfinish/', { booking_id: id })
        .then(() => location.reload())
        .catch(err => console.error(err));
});


// -------------------------------
// BOOKING → CANCEL
// -------------------------------
document.querySelector('.booking_cancel')?.addEventListener('click', () => {
    const card = getSelectedCard();
    if (!card) return alert("Select a booking first!");

    const id = card.dataset.id;

    sendPost('/business/markcancel/', { booking_id: id })
        .then(() => location.reload())
        .catch(err => console.error(err));
});


// -------------------------------
// REVIEW → SHOW
// -------------------------------
document.querySelector('.review_display_on')?.addEventListener('click', () => {
    const card = getSelectedCard();
    if (!card) return alert("Select a review first!");

    const id = card.dataset.id;

    sendPost('/business/unhide/', { review_id: id })
        .then(() => location.reload())
        .catch(err => console.error(err));
});


// -------------------------------
// REVIEW → HIDE
// -------------------------------
document.querySelector('.review_display_off')?.addEventListener('click', () => {
    const card = getSelectedCard();
    if (!card) return alert("Select a review first!");

    const id = card.dataset.id;

    sendPost('/business/hide/', { review_id: id })
        .then(() => location.reload())
        .catch(err => console.error(err));
});

