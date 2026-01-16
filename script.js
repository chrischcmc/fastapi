const apiUrl = "https://fastapi-amdb.onrender.com/movies/";
let moviesData = [];
let filteredData = [];
let sortColumn = null;
let sortDirection = 'asc';

// Fetch movies
fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
        moviesData = data;
        filteredData = data;
        renderTable(filteredData);
        updateStats();
    })
    .catch(error => {
        console.error("Error fetching movies:", error);
        document.getElementById("tableBody").innerHTML = 
            '<tr><td colspan="4" class="no-results">Error loading movies. Please try again later.</td></tr>';
    });

// Render table
function renderTable(data) {
    const tbody = document.getElementById("tableBody");
    
    if (data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="no-results">No movies found matching your search.</td></tr>';
        return;
    }

    tbody.innerHTML = data.map(movie => `
        <tr>
            <td class="id-cell">${movie.id}</td>
            <td class="title-cell">${movie.title}</td>
            <td class="director-cell">${movie.director}</td>
            <td class="year-cell">${movie.year}</td>
        </tr>
    `).join('');
}

// Search functionality
document.getElementById("searchInput").addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    
    filteredData = moviesData.filter(movie => 
        movie.title.toLowerCase().includes(searchTerm) ||
        movie.director.toLowerCase().includes(searchTerm) ||
        movie.year.toString().includes(searchTerm)
    );
    
    renderTable(filteredData);
    updateStats();
});

// Sorting functionality
document.querySelectorAll('th.sortable').forEach(header => {
    header.addEventListener('click', function() {
        const column = this.dataset.column;
        
        // Toggle sort direction
        if (sortColumn === column) {
            sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            sortColumn = column;
            sortDirection = 'asc';
        }
        
        // Update header classes
        document.querySelectorAll('th.sortable').forEach(h => {
            h.classList.remove('sorted-asc', 'sorted-desc');
        });
        this.classList.add(sortDirection === 'asc' ? 'sorted-asc' : 'sorted-desc');
        
        // Sort data
        filteredData.sort((a, b) => {
            let aVal = a[column];
            let bVal = b[column];
            
            if (typeof aVal === 'string') {
                aVal = aVal.toLowerCase();
                bVal = bVal.toLowerCase();
            }
            
            if (sortDirection === 'asc') {
                return aVal > bVal ? 1 : aVal < bVal ? -1 : 0;
            } else {
                return aVal < bVal ? 1 : aVal > bVal ? -1 : 0;
            }
        });
        
        renderTable(filteredData);
    });
});

// Update stats
function updateStats() {
    const stats = document.getElementById('stats');
    const showing = filteredData.length;
    const total = moviesData.length;
    
    if (showing === total) {
        stats.textContent = `Showing all ${total} movies`;
    } else {
        stats.textContent = `Showing ${showing} of ${total} movies`;
    }
}
