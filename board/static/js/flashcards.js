console.log("Flashcard script loaded");

let flashcards = [];
let currentCard = 0;

window.showCard = function(index) {
    if (flashcards.length > 0) {
        // Ensure index is within bounds
        if (index < 0 || index >= flashcards.length) {
            console.error("Index out of bounds:", index);
            return;
        }

        const card = flashcards[index].split(/\nDefinition:\s*/);
        document.getElementById('question').innerText = card[0].replace('Term: ', '').trim();
        document.getElementById('answer').innerText = card[1] ? card[1].trim() : "No answer available"; 
        document.querySelector('.flashcard').classList.remove('flipped');
    }
};

document.addEventListener("DOMContentLoaded", function() {
    const flashcardsData = document.getElementById('flashcards').getAttribute('data-flashcards');
    console.log("Raw flashcards data:", flashcardsData);
    console.log("Raw flashcards data length:", flashcardsData.length);

    if (!flashcardsData) {
        console.error("No flashcards data available.");
        return;
    }

    try {
        // Parse the data here
        flashcards = JSON.parse(flashcardsData);
        console.log("Parsed flashcards data:", flashcards);
    } catch (error) {
        console.error("Error parsing JSON:", error);
        return;
    }

    if (flashcards.length > 0) {
        showCard(currentCard);
    } else {
        console.warn("No flashcards available.");
    }
});

// Define flipCard and nextCard in the outer scope
window.flipCard = function() {
    document.querySelector('.flashcard').classList.toggle('flipped'); 
};

window.nextCard = function() {
    if (flashcards.length > 0) {
        currentCard = (currentCard + 1) % flashcards.length; 
        showCard(currentCard); 
    }
};
