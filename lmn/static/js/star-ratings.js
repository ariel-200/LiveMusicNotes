function renderStars() {
    const maxStars = 5;
    const starSize = "18px"
    const ratingElements = document.querySelectorAll('.note-rating');

    ratingElements.forEach(el => {  // loop through each el found
        const ratingValue = parseFloat(el.textContent.trim()); 
        
        if (!isNaN(ratingValue)) {  // just in case
            const filledStars = '★'.repeat(Math.min(Math.floor(ratingValue), maxStars));
            const emptyStars = '☆'.repeat(Math.max(0, maxStars - Math.floor(ratingValue)));
            
            el.textContent = filledStars + emptyStars;
            el.style.fontSize = starSize;
            
            el.style.color = "#3452ae";  // match colorscheme
        }
    });
}

document.addEventListener('DOMContentLoaded', renderStars);
