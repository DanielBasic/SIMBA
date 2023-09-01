// JavaScript for modal
const modal = document.getElementById("myModal");
const openModalBtn = document.getElementById("openModal");
const closeModalBtn = document.getElementById("closeModal");

openModalBtn.onclick = function () {
    modal.style.display = "block";
};

closeModalBtn.onclick = function () {
    modal.style.display = "none";
};

window.onclick = function (event) {
    if (event.target === modal) {
        modal.style.display = "none";
    }
};

// JavaScript for search filter
document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById("searchInput");
    const searchButton = document.getElementById("searchButton");
    const tableBody = document.getElementById("tableBody");
    const rows = tableBody.getElementsByTagName("tr");

    searchButton.addEventListener("click", performSearch);
    searchInput.addEventListener("input", performSearch);

    function performSearch() {
        const searchText = searchInput.value.toLowerCase();

        for (let i = 0; i < rows.length; i++) {
            const row = rows[i];
            const titleCell = row.querySelector("td:nth-child(2)"); // Assuming title is the second column
            if (titleCell) {
                const title = titleCell.innerHTML.toLowerCase();
                const shouldDisplay = title.includes(searchText);
                row.style.display = shouldDisplay ? "" : "none";
            }
        }
    }
});
