MAIN_CONTENT = document.getElementById("main-page");
SEARCH_CONTENT = document.getElementById("search-page");
SEARCH_INPUT = document.getElementById("thesearchbar");
CITY_SELECT = document.querySelector(".city-select");
RESULTS_CONTAINER = document.getElementById("searchResultsContainer");
ALL_CARDS = Array.from(document.querySelectorAll(".result-card")); // Static list of all cards

// --- 1. Content Toggling and Filter Trigger ---
function switchContent() {
    const query = SEARCH_INPUT.value.trim().toLowerCase();
    
    // 1. Toggle visibility based on input value
    if (query === "") {
        SEARCH_CONTENT.style.display = "none";
        MAIN_CONTENT.style.display = "block";
    } else {
        MAIN_CONTENT.style.display = "none";
        SEARCH_CONTENT.style.display = "block";
        
        // 2. Trigger the filtering
        filterAndDisplayResults();
    }
}
// Add event listeners to the city dropdown and search button to trigger filtering
CITY_SELECT.addEventListener('change', filterAndDisplayResults);
document.querySelector('.search-btn').addEventListener('click', filterAndDisplayResults);


// --- 2. Filtering Logic ---
function filterAndDisplayResults() {
    const query = SEARCH_INPUT.value.trim().toLowerCase();
    const city = CITY_SELECT.value.toLowerCase();
    
    let visibleCards = [];
    
    ALL_CARDS.forEach(card => {
        const name = card.dataset.name.toLowerCase();
        const cardCity = card.dataset.city.toLowerCase();
        
        // Check 1: Does the card match the text query (Name, Cuisine, or general search)?
        const nameMatch = name.includes(query);
        
        // Check 2: Does the card match the selected city?
        const cityMatch = (city === '' || cardCity.includes(city)); // Checks all if city select is general

        // If both conditions are met, show the card, otherwise hide it
        if (nameMatch || cityMatch) {
            card.style.display = 'flex'; // Use flex to maintain row layout
            visibleCards.push(card);
        } else {
            card.style.display = 'none';
        }
    });
    
    // After filtering, apply the active sort
    const activeSortButton = document.querySelector('.sorting-options .filter-btn.active');
    if (activeSortButton) {
        applySort(activeSortButton.dataset.sort, visibleCards);
    }
}


// --- 3. Sorting Logic ---
function applySort(sortType, cards) {
    cards.sort((a, b) => {
        let valA, valB;

        if (sortType === 'price') {
            valA = parseFloat(a.dataset.price);
            valB = parseFloat(b.dataset.price);
            return valA - valB; // Ascending price
        } else if (sortType === 'review') {
            valA = parseFloat(a.dataset.review); 
            valB = parseFloat(b.dataset.review);
            return valB - valA; 
        }
        return 0;
    });

    // Re-append the sorted cards to the container
    cards.forEach(card => RESULTS_CONTAINER.appendChild(card));
}


// --- 4. Toggles and Event Listeners ---
function initializeFiltersAndToggles() {
    // View Toggles (List/Grid)
    document.querySelectorAll('.view-btn').forEach(button => {
        button.addEventListener('click', function() {
            document.querySelectorAll('.view-btn').forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            if (this.dataset.view === 'grid') {
                RESULTS_CONTAINER.classList.remove('results-list');
                RESULTS_CONTAINER.classList.add('results-grid');
            } else {
                RESULTS_CONTAINER.classList.remove('results-grid');
                RESULTS_CONTAINER.classList.add('results-list');
            }
        });
    });

    // Sorting Toggles (Price/Date)
    document.querySelectorAll('.filter-btn').forEach(button => {
        button.addEventListener('click', function() {
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Re-filter and sort the currently visible cards
            const visibleCards = ALL_CARDS.filter(card => card.style.display !== 'none');
            applySort(this.dataset.sort, visibleCards);
        });
    });
}

// Ensure event listeners are set up once the DOM is ready
document.addEventListener('DOMContentLoaded', initializeFiltersAndToggles);