document.addEventListener('DOMContentLoaded', function() {
    const bidForm = document.querySelector('.bid-form');
    const bidInput = document.querySelector('#bidAmount');
    const currentPriceDisplay = document.querySelector('.listing-price');

    bidForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const listingId = this.closest('[data-listing-id]').getAttribute('data-listing-id');
        const bidAmount = parseFloat(bidInput.value);
        
        fetch(`/listing/${listingId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                form_type: 'bid',
                bid_amount: bidAmount
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update the displayed price
                currentPriceDisplay.textContent = `$${data.new_minimum_bid}`;
                bidInput.min = data.new_minimum_bid;
                bidInput.placeholder = `Minimum: $${data.new_minimum_bid}`;
                
                // Clear input and show success message
                bidInput.value = '';
                showNotification('Bid placed successfully!', 'success');
            } else {
                showNotification(data.error || 'Failed to place bid', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('An error occurred', 'error');
        });
    });
});

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `bid-notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
} 