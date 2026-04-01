var logoutButtons = document.querySelectorAll('#logout-button')

logoutButtons.forEach(function(button){
    button.addEventListener('click', function(ev){
        var okToLogout = confirm("Confirm Log Out?");
        if (!okToLogout) {
            ev.preventDefault();
        }
        alert("You are logged out!")
    })
})
