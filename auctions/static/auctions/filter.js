document.addEventListener("DOMContentLoaded", () => {
    const categorySelect = document.getElementById("category-select");
    const sizeSelect = document.getElementById("size-select");
    const conditionSelect = document.getElementById("condition-select");

    categorySelect.addEventListener("change", () => filterItems());
    sizeSelect.addEventListener("change", () => filterItems());
    conditionSelect.addEventListener("change", () => filterItems());

    function filterItems() {


        const listings = document.querySelectorAll("#listings .grid-listing"); // Get all listings
        console.log("listings:", listings); // Log the NodeList of listings


        

        const selectedCategory = categorySelect.value;
        const selectedSize = sizeSelect.value;
        const selectedCondition = conditionSelect.value;
        console.log(document.getElementById("category-select"));

        listings.forEach(listing => {
            console.log("fart")


            
            // Retrieve the data attributes for this listing
            const itemCategory = listing.dataset.category;
            const itemSize = listing.dataset.size;
            const itemCondition = listing.dataset.condition;

            // Check if the listing matches the selected filters
            const matchesCategory = selectedCategory === "all" || itemCategory === selectedCategory;
            const matchesSize = selectedSize === "all" || itemSize === selectedSize;
            const matchesCondition = selectedCondition === "all" || itemCondition === selectedCondition;

            // Show or hide the listing based on the filter criteria
            if (matchesCategory && matchesSize && matchesCondition) {
                listing.style.display = "block"; // Show matching items
            } else {
                listing.style.display = "none"; // Hide non-matching items
            }
        });
    }
});