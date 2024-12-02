// Sample book data
const books = [
    { title: "Book Title 1", author: "Author Name", image: "book1.jpg" },
    { title: "Book Title 2", author: "Author Name", image: "book2.jpg" },
    { title: "Book Title 3", author: "Author Name", image: "book3.jpg" },
    { title: "Another Book", author: "Different Author", image: "book4.jpg" },
];

// Function to filter books based on user input
function filterBooks() {
    const query = document.getElementById("searchBar").value.toLowerCase();
    const resultsDiv = document.getElementById("searchResults");
    resultsDiv.innerHTML = ""; // Clear previous results

    // Filter books based on title matching the query
    const filteredBooks = books.filter((book) =>
        book.title.toLowerCase().includes(query)
    );

    // Display filtered books
    if (filteredBooks.length > 0) {
        filteredBooks.forEach((book) => {
            const bookCard = `
                <div class="book-card">
                    <img src="${book.image}" alt="${book.title}">
                    <h3>${book.title}</h3>
                    <p>Author: ${book.author}</p>
                </div>
            `;
            resultsDiv.innerHTML += bookCard;
        });
    } else {
        resultsDiv.innerHTML = `<p>No books found for "${query}"</p>`;
    }
}
