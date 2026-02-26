document.getElementById('fitness-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
        duration: parseFloat(document.getElementById('duration').value),
        heart_rate: parseFloat(document.getElementById('heart_rate').value),
        bmi: parseFloat(document.getElementById('bmi').value),
        age: parseFloat(document.getElementById('age').value)
    };

    const loading = document.getElementById('loading');
    const resultCard = document.getElementById('result-card');
    const calValue = document.getElementById('calorie-value');
    const meterFill = document.getElementById('meter-fill');

    loading.classList.remove('hidden');
    resultCard.classList.add('hidden');

    try {
        const response = await fetch('http://localhost:8001/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.error) throw new Error(result.error);

        // Animate count up
        const target = result.calories_burned;
        let current = 0;
        const speed = target / 50;

        calValue.innerText = '0';
        loading.classList.add('hidden');
        resultCard.classList.remove('hidden');

        const timer = setInterval(() => {
            current += speed;
            if (current >= target) {
                calValue.innerText = Math.round(target);
                clearInterval(timer);
            } else {
                calValue.innerText = Math.round(current);
            }
        }, 20);

        // Animate meter
        const percentage = Math.min((target / 1000) * 100, 100);
        setTimeout(() => {
            meterFill.style.width = percentage + '%';
        }, 100);

    } catch (error) {
        alert("Error: " + error.message + "\nMake sure the backend is running (main.py)");
        loading.classList.add('hidden');
    }
});
