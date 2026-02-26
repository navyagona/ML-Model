document.getElementById('prediction-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = {
        sepal_length: parseFloat(document.getElementById('sepal_length').value),
        sepal_width: parseFloat(document.getElementById('sepal_width').value),
        petal_length: parseFloat(document.getElementById('petal_length').value),
        petal_width: parseFloat(document.getElementById('petal_width').value),
    };

    const loading = document.getElementById('loading');
    const resultContainer = document.getElementById('result-container');
    const predictBtn = document.getElementById('predict-btn');

    // Show loading state
    loading.classList.remove('hidden');
    resultContainer.classList.add('hidden');
    predictBtn.disabled = true;

    try {
        const response = await fetch('http://localhost:8000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        });

        if (!response.ok) {
            throw new Error('API request failed');
        }

        const data = await response.json();

        // Update UI with results
        const speciesEl = document.getElementById('predicted-species');
        const confidenceBar = document.getElementById('confidence-bar');
        const confidenceVal = document.getElementById('confidence-value');

        speciesEl.textContent = data.species;
        
        // Dynamic coloring based on species
        speciesEl.style.color = `var(--accent-${data.species})`;
        confidenceBar.style.backgroundColor = `var(--accent-${data.species})`;

        const confPercent = (data.confidence * 100).toFixed(1) + '%';
        confidenceVal.textContent = confPercent;
        
        // Trigger bar animation
        setTimeout(() => {
            confidenceBar.style.width = confPercent;
        }, 100);

        // Show result container
        resultContainer.classList.remove('hidden');
    } catch (error) {
        console.error('Error:', error);
        alert('Make sure the FastAPI server is running locally (main.py)');
    } finally {
        loading.classList.add('hidden');
        predictBtn.disabled = false;
    }
});
