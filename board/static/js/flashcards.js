console.log("Flashcard script loaded");

let flashcards = [];
let currentCard = 0;

window.showCard = function(index) {
    console.log("Showing card at index:", index);
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

document.addEventListener("DOMContentLoaded", function () {
    const flashcardsElement = document.getElementById('flashcards');
    const flashcardsData = flashcardsElement.getAttribute('data-flashcards');
    console.log(flashcardsElement);
    console.log(flashcardsData);

    if (flashcardsData) {
        try {
            const flashcards = JSON.parse(flashcardsData);

            // Now you can use the flashcards array
            console.log(flashcards); // Check the parsed output

            // Example: Display the flashcards
            flashcards.forEach(card => {
                // Your logic to display each flashcard
                console.log(card);
            });
        } catch (error) {
            console.error("Error parsing flashcards JSON:", error);
        }
    } else {
        console.warn("No flashcards data available.");
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
