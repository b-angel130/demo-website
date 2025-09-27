const sidebarLinks = document.querySelectorAll('.sidebar ul li a');

// Get current path without language prefix
let currentUrl = window.location.pathname.replace(/\/$/, ""); // remove trailing slash

// Remove possible language code at the start (e.g., /en, /fa, /it)
currentUrl = currentUrl.replace(/^\/(en|fa|it)/, '');

sidebarLinks.forEach(link => {
    // Remove trailing slash and language prefix from link href
    let linkPath = link.getAttribute('href').replace(/\/$/, "");
    linkPath = linkPath.replace(/^\/(en|fa|it)/, '');

    if(linkPath === currentUrl){
        link.style.backgroundColor = '#3498db';
        link.style.color = 'white';
    }
});
