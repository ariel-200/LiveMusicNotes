var logoutButtons = document.querySelectorAll('#logout-button')

logoutButtons.forEach(function(button){
    button.addEventListener('click', function(ev){
        var okToLogout = confirm("Confirm Log Out?");
        if (!okToLogout) {
            ev.preventDefault();
        }
    })
})

// store logout in session
document.addEventListener('DOMContentLoaded', () => {
    if (sessionStorage.getItem('loggedOut') === 'true') {
        alert("You have logged out!");
        sessionStorage.removeItem('loggedOut');
    }
    const logoutForm = document.getElementById('logout-form');
    if (logoutForm) {
        logoutForm.addEventListener('submit', () => {
            sessionStorage.setItem('loggedOut', 'true');
        });
    }
});
