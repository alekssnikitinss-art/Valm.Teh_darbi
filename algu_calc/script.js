document.getElementById('calculateBtn').addEventListener('click', function() {
    // Get input values
    const salary = parseFloat(document.getElementById('salary').value);
    const taxRate = parseFloat(document.getElementById('tax_rate').value);
    
    // Validate inputs
    if (isNaN(salary) || salary < 0 || isNaN(taxRate) || taxRate < 0) {
        alert('Please enter valid values');
        return;
    }
    
    // Calculate
    const taxAmount = salary * (taxRate / 100);
    const netSalary = salary - taxAmount;
    
    // Display results
    document.getElementById('grossSalary').textContent = '€' + salary.toFixed(2);
    document.getElementById('taxAmount').textContent = '€' + taxAmount.toFixed(2);
    document.getElementById('netSalary').textContent = '€' + netSalary.toFixed(2);
    
    // Show results container
    document.getElementById('results').style.display = 'block';
    
    // Optional: Display an image (change URL to your image path)
    const resultImage = document.getElementById('resultImage');
    resultImage.src = 'https://via.placeholder.com/300x200?text=Salary+Calculated'; // Replace with your image
    resultImage.style.display = 'block';
});