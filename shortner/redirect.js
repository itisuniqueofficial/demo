// Load URLs from the JSON file
fetch('urls.json')
    .then(response => response.json())
    .then(data => {
        const urlMap = {};
        data.urls.forEach(item => {
            urlMap[item.key] = item.url;
        });

        // Redirect based on the hash part of the URL
        const key = window.location.hash.substring(1);
        if (urlMap.hasOwnProperty(key)) {
            window.location.href = urlMap[key];
        } else {
            document.write('URL not found');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.write('An error occurred');
    });
