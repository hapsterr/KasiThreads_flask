document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('mobile-menu');
    const mobileNav = document.getElementById('mobile-nav');
    const closeBar = document.getElementById('close-bar');  // Add this line

    // Function to open the mobile nav
    menuToggle.addEventListener('click', function() {
        mobileNav.classList.toggle('open');
    });

    // Function to close the mobile nav
    closeBar.addEventListener('click', function() {  
        mobileNav.classList.remove('open');  
    });
});


document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('cart').addEventListener('click', function(event) {
        event.preventDefault();
        const iframeContainer = document.getElementById('iframeContainer');
        const iframe = document.getElementById('iframe');
        
        iframe.src = '/cart';
        iframeContainer.style.display = 'block';
    });
});

function closeIframe() {
    const iframeContainer = document.getElementById('iframeContainer');
    iframeContainer.style.display = 'none';
    document.getElementById('iframe').src = ''; 
}