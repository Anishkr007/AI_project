document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const resultDiv = document.getElementById('result');
    const predictButton = document.getElementById('predict-button');

    // The URL of your Flask backend's predict endpoint
    // If you run Flask locally, it's usually this.
    const apiUrl = 'http://127.0.0.1:5000/predict';

    form.addEventListener('submit', (e) => {
        e.preventDefault(); // Prevent the form from submitting normally

        // Change button to "Loading..."
        const originalButtonText = predictButton.textContent;
        predictButton.textContent = 'Predicting...';
        predictButton.disabled = true;

        // Collect data from the form
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        // Send the data to the backend API
        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => {
            if (!response.ok) {
                // Handle HTTP errors
                throw new Error(`Network response was not ok (${response.status})`);
            }
            return response.json();
        })
        .then(result => {
            // Display the prediction
            if (result.prediction) {
                const predictedPrice = result.prediction.toFixed(2);
                resultDiv.textContent = `₹ ${predictedPrice} Lakhs`;
            } else if (result.error) {
                // Display error from backend
                resultDiv.textContent = `Error: ${result.error}`;
            }
        })
        .catch(error => {
            // Display network or other errors
            console.error('Error:', error);
            resultDiv.textContent = 'Error: Could not get prediction. Is the backend server running?';
        })
        .finally(() => {
            // Restore button
            predictButton.textContent = originalButtonText;
            predictButton.disabled = false;
        });
    });
});