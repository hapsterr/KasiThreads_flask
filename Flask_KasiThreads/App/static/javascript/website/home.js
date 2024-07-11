document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contact-form');

    contactForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const serviceID = 'service_ilpnetl'; // Replace with your EmailJS service ID
        const templateID = 'template_spix82a'; // Replace with your EmailJS template ID

        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            message: document.getElementById('message').value
        };

        emailjs.send(serviceID, templateID, formData)
            .then(() => {
                alert('Message sent successfully!');

                // Send auto-reply to user
                emailjs.send(serviceID, template_e02bx6q, formData)
                    .then(() => {
                        console.log('Auto-reply sent successfully!');
                    }, (error) => {
                        console.error('Failed to send auto-reply...', error);
                    });

                contactForm.reset();
            }, (error) => {
                alert('Failed to send message. Please try again.');
                console.error('Failed...', error);
            });
    });
});



document.addEventListener('DOMContentLoaded', function() {
    const scrollbrands = document.querySelector('.scroll-brands');
    const prevBtn = document.querySelector('.prev');
    const nextBtn = document.querySelector('.next');

    // Event listener for previous button
    prevBtn.addEventListener('click', function(){
        scrollbrands.scrollLeft -= 200;
    });

    nextBtn.addEventListener('click', function() {
        scrollbrands.scrollLeft += 200;
    });
    setInterval(function() {
        scrollbrands.scrollLeft += 200;
    }, 10000);
   
});


document.addEventListener('DOMContentLoaded', function() {
    const scrollContainer = document.querySelector('.scroll-content');
    const prevBtn = document.querySelector('.prevprod');
    const nextBtn = document.querySelector('.nextprod');

    // Event listener for previous button
    prevBtn.addEventListener('click', function() {
        scrollContainer.scrollLeft -= 200;
    });

    // Event listener for next button
    nextBtn.addEventListener('click', function() {
        scrollContainer.scrollLeft += 200;
    });
   
    setInterval(function() {
        scrollContainer.scrollLeft += 200;
    }, 6000);
});