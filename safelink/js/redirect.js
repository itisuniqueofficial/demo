window.onload = function () {
    var urlParams = new URLSearchParams(window.location.search);
    var encodedURL = urlParams.get('url');
    var originalURL = atob(encodedURL); // Decode Base64 URL

    var countdown = 30; // Countdown time in seconds

    var countdownInterval = setInterval(function () {
        document.getElementById("countdown").textContent = countdown;
        countdown--;

        if (countdown < 0) {
            clearInterval(countdownInterval);
            document.getElementById("goButton").style.display = 'block'; // Show the Go button
            document.getElementById("goButton").onclick = function () {
                window.location.href = originalURL; // Redirect when clicked
            };
        }
    }, 1000); // Update countdown every second
}

document.addEventListener('DOMContentLoaded', function () {
    // Define the desired domain
    var desiredDomain = 'demo.itisuniqueblog.com';

    // Extract the current domain from the URL
    var currentDomain = window.location.hostname;

    // Check if the current domain does not match the desired domain
    if (currentDomain !== desiredDomain) {
        // Redirect to the desired URL
        window.location.href = 'https://cdn.itisuniqueblog.com';
    }
});
