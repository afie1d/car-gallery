function searchReviews() {
    const keywords = document.getElementById('searchInput').value;

    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ keywords: keywords }),
    })
    .then(response => response.json())
    .then(data => displayResults(data))
    .catch(error => console.error('Error:', error));
}

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = ''; // Clear previous results

    data.forEach(item => {
        const resultItem = document.createElement('div');
        resultItem.classList.add('result-item');

        const carName = document.createElement('div');
        carName.classList.add('car-name');
        carName.innerText = item.name;

        const reviewText = document.createElement('div');
        reviewText.classList.add('review-text');
        reviewText.innerText = item.review;

        resultItem.appendChild(carName);
        resultItem.appendChild(reviewText);
        resultsDiv.appendChild(resultItem);
    });
}