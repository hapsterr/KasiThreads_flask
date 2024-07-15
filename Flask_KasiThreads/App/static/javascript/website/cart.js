
function deleteFromCart(product_id) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    cart = cart.filter(item => !(item.productId === product_id));
    localStorage.setItem('cart', JSON.stringify(cart));

    // Update the cart on the server side
    fetch('/cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ cart: cart })
    }).then(response => {
        if (response.redirected) {
            window.location.href = '/cart';
        }
    }).catch(error => {
        console.error('Error:', error);
        alert('Failed to update cart. Please try again.');
    });
}