document.addEventListener("DOMContentLoaded", function() {
    // Fetch flashcards data from the hidden div
    let flashcards = JSON.parse(document.getElementById('flashcards').getAttribute('data-flashcards'));
    let currentCard = 0;

    // Check if flashcards array is not empty
    if (flashcards.length > 0) {
        showCard(currentCard);
    } else {
        console.warn("No flashcards available.");
    }

    function showCard(index) {
        if (flashcards.length > 0) {
            // Split the card content into term and definition
            const card = flashcards[index].split(/\nDefinition:\s*/);
            
            // Update the front (question) and back (answer) of the flashcard
            document.getElementById('question').innerText = card[0].replace('Term: ', '').trim(); // Extract the term
            document.getElementById('answer').innerText = card[1] ? card[1].trim() : "No answer available"; // Extract the definition or set a default
            document.querySelector('.flashcard').classList.remove('flipped');
        }
    }  

    // Define flipCard function
    window.flipCard = function() {
        document.querySelector('.flashcard').classList.toggle('flipped'); 
    };

    // Define nextCard function
    window.nextCard = function() {
        if (flashcards.length > 0) {
            currentCard = (currentCard + 1) % flashcards.length; 
            showCard(currentCard); 
        }
    };
});
