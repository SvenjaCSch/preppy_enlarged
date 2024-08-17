console.log("Flashcard script loaded");

let flashcards = [];
let currentCard = 0;

// Function to display a flashcard
window.showCard = function(index) {
    console.log("Showing card at index:", index);
    if (flashcards.length > 0) {
        // Ensure index is within bounds
        if (index < 0 || index >= flashcards.length) {
            console.error("Index out of bounds:", index);
            return;
        }

        // Get the current card
        const card = flashcards[index];
        // Display the term (question) and definition (answer)
        document.getElementById('question').innerText = card.Term.trim();
        document.getElementById('answer').innerText = card.Definition.trim() || "No answer available";
        // Ensure the card is showing the front side
        document.querySelector('.flashcard').classList.remove('flipped');
    }
};

// Function to flip the flashcard
window.flipCard = function() {
    document.querySelector('.flashcard').classList.toggle('flipped');
};

// Function to show the next flashcard
window.nextCard = function() {
    if (flashcards.length > 0) {
        // Increment the current card index, wrap around if necessary
        currentCard = (currentCard + 1) % flashcards.length;
        showCard(currentCard);
    }
};

// Initialize the flashcards when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function () {
    // Retrieve the flashcards data from the data-flashcards attribute
    const flashcardsElement = document.getElementById('flashcards');
    flashcards = JSON.parse(flashcardsElement.dataset.flashcards);

    // Check if there are any flashcards, and display the first one if there are
    if (flashcards && flashcards.length > 0) {
        showCard(currentCard);
    } else {
        console.warn("No flashcards data available.");
    }
});
