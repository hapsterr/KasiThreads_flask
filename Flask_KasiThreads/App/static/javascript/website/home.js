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


//Adding home photos to html
async function fetchJSON() {
    const response = await fetch('homephotos.json');
    const data = await response.json();
    displayData(data);
}

function displayData(data) {
    const jsonDataDiv = document.getElementById('Home-photos');
    const jsonSecondThirdDiv = document.getElementById('secondthird');
    jsonSecondThirdDiv.innerHTML = '';
    
   data.HomePhotos.forEach(photo => {
        const photoDiv = document.createElement('div');
        photoDiv.classList.add(photo.id);
        photoDiv.style.backgroundImage = `url('${photo.url}')`;
        photoDiv.innerHTML = `
            <h3>${photo.heading}</h3>
            <h2>${photo.category}</h2>
            <h1>${photo.description}</h1>
        `;
        jsonDataDiv.appendChild(photoDiv);
    });
    data.HomeRightPhotos.forEach(photo => {
        const photoDiv = document.createElement('div');
        photoDiv.classList.add(photo.id);
        photoDiv.style.backgroundImage = `url('${photo.url}')`;
        photoDiv.innerHTML = `
            <h3>${photo.heading}</h3>
            <h2>${photo.category}</h2>
            <h1>${photo.description}</h1>
        `;
        jsonSecondThirdDiv.appendChild(photoDiv);
    });
}


fetchJSON();