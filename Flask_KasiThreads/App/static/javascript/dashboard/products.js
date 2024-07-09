function deleteProduct(productId) {
    fetch(`/delete_product/${productId}`, {
        method: 'DELETE'
    }).then(response => {
        if (response.ok) {
            document.querySelector(`.product[data-id="${productId}"]`).remove();
        } else {
            alert('Failed to delete product.');
        }
    });
}