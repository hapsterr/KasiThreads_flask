function addToCart(productId) {
    // Retrieve selected quantity and size
    let quantity = parseInt(document.getElementById('quantity').value);
    let sizeInputs = document.getElementsByName('size');
    let size;

    for (let i = 0; i < sizeInputs.length; i++) {
        if (sizeInputs[i].checked) {
            size = sizeInputs[i].value;
            break;
        }
    }

    if (!quantity || !size) {
        alert('Please select quantity and size.');
        return;
    }

    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    // Check if the product already exists in the cart
    let existingProduct = cart.find(item => item.productId === productId && item.size === size);

    if (existingProduct) {
        // Update the quantity of the existing product
        alert('Product already added to cart!');
    } else {
        // Add the new product with productId, quantity, and size to the cart
        cart.push({ "productId": productId, "quantity": quantity, "size": size });
        alert('Product added to cart!');
    }

    localStorage.setItem('cart', JSON.stringify(cart));

    fetch('/cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ cart: cart })
    }).then(response => {
        if (response.redirected) {
            window.location.href = '/shop';
        }
    }).catch(error => {
        console.error('Error:', error);
        alert('Failed to add product to cart. Please try again.');
    });
}