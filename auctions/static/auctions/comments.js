document.addEventListener('DOMContentLoaded', function() {
    const commentForm = document.querySelector('.comment-form');
    const commentsContainer = document.querySelector('.comments-container');

    commentForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const commentInput = document.querySelector('#comment');
        const listingId = this.getAttribute('data-listing-id');
        
        fetch(`/listing/${listingId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                content: commentInput.value
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const date = new Date(data.comment.created_at);
                const formattedDate = `${(date.getMonth() + 1).toString().padStart(2, '0')}.${date.getDate().toString().padStart(2, '0')}.${date.getFullYear()}`;
                const time = date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true });
                
                // Check if we need to add a new date header
                const lastDateHeader = Array.from(commentsContainer.querySelectorAll('.comment-date')).pop();
                if (!lastDateHeader || lastDateHeader.textContent !== formattedDate) {
                    const dateHeader = document.createElement('div');
                    dateHeader.className = 'comment-date';
                    dateHeader.textContent = formattedDate;
                    commentsContainer.appendChild(dateHeader);
                }
                
                // Create and append new comment
                const newComment = createCommentElement(data.comment, time);
                commentsContainer.appendChild(newComment);
                
                // Clear input field
                commentInput.value = '';
                
                // Remove "no comments" message if it exists
                const noCommentsMsg = commentsContainer.querySelector('.no-comments');
                if (noCommentsMsg) {
                    noCommentsMsg.remove();
                }
                
                // Scroll to the bottom to show the new comment
                commentsContainer.scrollTop = commentsContainer.scrollHeight;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

function createCommentElement(comment, time) {
    const commentDiv = document.createElement('div');
    commentDiv.className = 'comment';
    
    commentDiv.innerHTML = `
        <p><strong>${comment.username}:</strong> ${comment.content} <small style="color: #888; float: right;">${time}</small></p>
    `;
    return commentDiv;
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