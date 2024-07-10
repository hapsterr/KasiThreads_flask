function deleteProduct(productId) {
    fetch(`/delete_product/${productId}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (response.ok) {
            // Remove the product element from the DOM
            document.querySelector(`.product[data-id="${productId}"]`).remove();
        } else {
            // Handle failure to delete product
            alert('Failed to delete product. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while deleting the product.');
    });
}