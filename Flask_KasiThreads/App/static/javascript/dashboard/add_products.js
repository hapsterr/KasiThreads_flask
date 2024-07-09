function updateSizeOptions() {
    const typeSelect = document.getElementById('type');
    const sizeContainer = document.getElementById('size'); 
    const type = typeSelect.value;

    sizeContainer.innerHTML = '';

    if (type === 'shoes') {
        for (let i = 1; i <= 11; i++) {
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.id = 'size' + i; 
            checkbox.name = 'size'; 
            checkbox.value = 'UK ' + i; 
            const label = document.createElement('label');
            label.textContent = 'UK ' + i; 
            label.setAttribute('for', 'size' + i); 
            sizeContainer.appendChild(checkbox); 
            sizeContainer.appendChild(label); 
            sizeContainer.appendChild(document.createElement('br')); 
        }
    } else if (type === 'clothing') {
        const sizes = ['XS', 'S', 'M', 'L', 'XL'];
        sizes.forEach(size => {
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.id = 'size' + size; 
            checkbox.name = 'size'; 
            checkbox.value = size; 
            const label = document.createElement('label');
            label.textContent = size; 
            label.setAttribute('for', 'size' + size); 
            sizeContainer.appendChild(checkbox); 
            sizeContainer.appendChild(label); 
            sizeContainer.appendChild(document.createElement('br')); 
        });
    }
}