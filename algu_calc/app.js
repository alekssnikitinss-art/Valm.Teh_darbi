// ========================================
// SALARY CALCULATOR CONFIGURATION
// ========================================
const CONFIG = {
    VSAOI_RATE: 10.5,           // Employee social security
    IIN_RATE: 20,               // Personal income tax
    EMPLOYER_VSAOI_RATE: 13.6,  // Employer social security
    NON_TAXABLE_MINIMUM: 500,   // EUR per month
    DEPENDENT_DEDUCTION: 250,   // EUR per dependent
    USE_TAX_BOOKLET: false,     // Tax booklet status
};

// ========================================
// DOM ELEMENTS
// ========================================
const elements = {
    // Inputs
    salary: document.getElementById('salary'),
    direction: document.querySelectorAll('input[name="direction"]'),
    vsaoi: document.getElementById('vsaoi'),
    iin: document.getElementById('iin'),
    employerVsaoi: document.getElementById('employer-vsaoi'),
    dependents: document.getElementById('dependents'),
    taxBooklet: document.getElementById('taxBooklet'),
    deductionsEnabled: document.getElementById('deductionsEnabled'),
    
    // Buttons
    calculateBtn: document.getElementById('calculateBtn'),
    clearBtn: document.getElementById('clearBtn'),
    
    // Output
    results: document.getElementById('results'),
    errorMessage: document.getElementById('errorMessage'),
    
    // Result Values
    netSalary: document.getElementById('netSalary'),
    grossSalary: document.getElementById('grossSalary'),
    vsaoiDeduction: document.getElementById('vsaoiDeduction'),
    iinDeduction: document.getElementById('iinDeduction'),
    totalDeductions: document.getElementById('totalDeductions'),
    employerVsaoiValue: document.getElementById('employerVsaoi'),
    totalEmployerCost: document.getElementById('totalEmployerCost'),
    
    // Detailed View
    detailedView: document.getElementById('detailedView'),
    detailedTable: document.getElementById('detailedTable'),
};

// ========================================
// EVENT LISTENERS
// ========================================
elements.calculateBtn.addEventListener('click', handleCalculate);
elements.clearBtn.addEventListener('click', handleClear);
elements.detailedView.addEventListener('change', toggleDetailedView);
elements.salary.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleCalculate();
});

// ========================================
// MAIN CALCULATION FUNCTION
// ========================================
function handleCalculate() {
    // Clear previous errors
    hideError();
    
    // Get values
    const salary = parseFloat(elements.salary.value);
    const direction = Array.from(elements.direction).find(r => r.checked).value;
    const dependents = parseInt(elements.dependents.value) || 0;
    const taxBooklet = elements.taxBooklet.checked;
    const deductionsEnabled = elements.deductionsEnabled.checked;
    
    // Get tax rates
    const vsaoiRate = parseFloat(elements.vsaoi.value) || CONFIG.VSAOI_RATE;
    const iinRate = parseFloat(elements.iin.value) || CONFIG.IIN_RATE;
    const employerVsaoiRate = parseFloat(elements.employerVsaoi.value) || CONFIG.EMPLOYER_VSAOI_RATE;
    
    // Validation
    const error = validateInput(salary, dependents);
    if (error) {
        showError(error);
        return;
    }
    
    // Calculate based on direction
    let result;
    if (direction === 'bruto-to-neto') {
        result = calculateBrutoToNeto(salary, vsaoiRate, iinRate, employerVsaoiRate, dependents, taxBooklet, deductionsEnabled);
    } else {
        result = calculateNetoToBruto(salary, vsaoiRate, iinRate, employerVsaoiRate, dependents, taxBooklet, deductionsEnabled);
    }
    
    // Display results
    displayResults(result);
}

// ========================================
// BRUTO TO NETO CALCULATION
// ========================================
function calculateBrutoToNeto(bruto, vsaoiRate, iinRate, employerVsaoiRate, dependents, taxBooklet, deductionsEnabled) {
    // Calculate deductions for employee
    let vsaoiDeduction = bruto * (vsaoiRate / 100);
    let iinDeduction = calculateIIN(bruto, vsaoiDeduction, iinRate, dependents, taxBooklet, deductionsEnabled);
    
    // Calculate net salary
    const neto = bruto - vsaoiDeduction - iinDeduction;
    
    // Calculate employer costs
    const employerVsaoi = bruto * (employerVsaoiRate / 100);
    const totalEmployerCost = bruto + employerVsaoi;
    
    return {
        bruto: bruto,
        neto: neto,
        vsaoiDeduction: vsaoiDeduction,
        iinDeduction: iinDeduction,
        employerVsaoi: employerVsaoi,
        totalEmployerCost: totalEmployerCost,
        totalDeductions: vsaoiDeduction + iinDeduction,
    };
}

// ========================================
// NETO TO BRUTO CALCULATION (Binary Search)
// ========================================
function calculateNetoToBruto(neto, vsaoiRate, iinRate, employerVsaoiRate, dependents, taxBooklet, deductionsEnabled) {
    // Use binary search for robust convergence
    let minBruto = neto;  // Minimum possible bruto
    let maxBruto = neto * 3;  // Maximum possible bruto (safeguard)
    
    // Find reasonable upper bound
    for (let attempt = 0; attempt < 10; attempt++) {
        const result = calculateBrutoToNeto(maxBruto, vsaoiRate, iinRate, employerVsaoiRate, dependents, taxBooklet, deductionsEnabled);
        if (result.neto >= neto) {
            break;  // Found upper bound
        }
        maxBruto *= 2;
        if (maxBruto > 1000000) {
            // Safety check - something is very wrong
            return calculateBrutoToNeto(neto * 1.5, vsaoiRate, iinRate, employerVsaoiRate, dependents, taxBooklet, deductionsEnabled);
        }
    }
    
    // Binary search for exact bruto value
    for (let i = 0; i < 50; i++) {
        const midBruto = (minBruto + maxBruto) / 2;
        const result = calculateBrutoToNeto(midBruto, vsaoiRate, iinRate, employerVsaoiRate, dependents, taxBooklet, deductionsEnabled);
        const diff = result.neto - neto;
        
        // If we're close enough, return
        if (Math.abs(diff) < 0.01) {
            return result;
        }
        
        // Adjust search bounds
        if (diff < 0) {
            minBruto = midBruto;  // Neto too low, need higher bruto
        } else {
            maxBruto = midBruto;  // Neto too high, need lower bruto
        }
    }
    
    // Return best approximation found
    const finalBruto = (minBruto + maxBruto) / 2;
    return calculateBrutoToNeto(finalBruto, vsaoiRate, iinRate, employerVsaoiRate, dependents, taxBooklet, deductionsEnabled);
}

// ========================================
// IIN (PERSONAL INCOME TAX) CALCULATION
// ========================================
function calculateIIN(bruto, vsaoi, iinRate, dependents, taxBooklet, deductionsEnabled) {
    // Base for IIN calculation
    let iinBase = bruto - vsaoi;
    
    // Apply tax booklet deduction if enabled
    let nonTaxableAmount = 0;
    if (taxBooklet && deductionsEnabled) {
        nonTaxableAmount = CONFIG.NON_TAXABLE_MINIMUM;
    }
    
    // Apply dependent deductions if enabled
    if (deductionsEnabled) {
        nonTaxableAmount += dependents * CONFIG.DEPENDENT_DEDUCTION;
    }
    
    // Calculate taxable base
    const taxableBase = Math.max(iinBase - nonTaxableAmount, 0);
    
    // Calculate IIN
    const iin = taxableBase * (iinRate / 100);
    
    return iin;
}

// ========================================
// VALIDATION
// ========================================
function validateInput(salary, dependents) {
    // Support both comma and period as decimal separator
    if (isNaN(salary) || salary <= 0) {
        return 'Lūdzu, ievadi derīgu summu';
    }
    
    if (salary > 1000000) {
        return 'Summa pārāk liela. Lūdzu, pārbaudī ievadi.';
    }
    
    if (dependents < 0 || dependents > 20) {
        return 'Apgādājamo skaits jābūt starp 0 un 20';
    }
    
    return null;
}

// ========================================
// DISPLAY RESULTS
// ========================================
function displayResults(result) {
    // Update summary values
    elements.netSalary.textContent = formatCurrency(result.neto);
    elements.grossSalary.textContent = formatCurrency(result.bruto);
    
    // Update deductions
    elements.vsaoiDeduction.textContent = formatCurrency(result.vsaoiDeduction);
    elements.iinDeduction.textContent = formatCurrency(result.iinDeduction);
    elements.totalDeductions.textContent = formatCurrency(result.totalDeductions);
    
    // Update employer costs
    elements.employerVsaoiValue.textContent = formatCurrency(result.employerVsaoi);
    elements.totalEmployerCost.textContent = formatCurrency(result.totalEmployerCost);
    
    // Update detailed table if visible
    if (elements.detailedView.checked) {
        updateDetailedTable(result);
    }
    
    // Show results
    elements.results.style.display = 'block';
    elements.results.scrollIntoView({ behavior: 'smooth' });
}

// ========================================
// UPDATE DETAILED TABLE
// ========================================
function updateDetailedTable(result) {
    const bruto = result.bruto;
    const neto = result.neto;
    const vsaoi = result.vsaoiDeduction;
    const iin = result.iinDeduction;
    const employerVsaoi = result.employerVsaoi;
    
    document.getElementById('dt-bruto').textContent = formatCurrency(bruto);
    document.getElementById('dt-vsaoi-pct').textContent = formatPercent(vsaoi / bruto * 100);
    document.getElementById('dt-vsaoi').textContent = formatCurrency(vsaoi);
    
    document.getElementById('dt-iin-pct').textContent = formatPercent(iin / bruto * 100);
    document.getElementById('dt-iin').textContent = formatCurrency(iin);
    
    document.getElementById('dt-neto-pct').textContent = formatPercent(neto / bruto * 100);
    document.getElementById('dt-neto').textContent = formatCurrency(neto);
    
    document.getElementById('dt-emp-vsaoi-pct').textContent = formatPercent(employerVsaoi / bruto * 100);
    document.getElementById('dt-emp-vsaoi').textContent = formatCurrency(employerVsaoi);
}

// ========================================
// TOGGLE DETAILED VIEW
// ========================================
function toggleDetailedView() {
    if (elements.detailedView.checked) {
        elements.detailedTable.style.display = 'block';
    } else {
        elements.detailedTable.style.display = 'none';
    }
}

// ========================================
// CLEAR FORM
// ========================================
function handleClear() {
    elements.salary.value = '';
    elements.dependents.value = '0';
    elements.taxBooklet.checked = false;
    elements.deductionsEnabled.checked = true;
    elements.detailedView.checked = false;
    elements.results.style.display = 'none';
    elements.detailedTable.style.display = 'none';
    hideError();
    elements.salary.focus();
}

// ========================================
// ERROR HANDLING
// ========================================
function showError(message) {
    elements.errorMessage.textContent = message;
    elements.errorMessage.style.display = 'block';
    elements.results.style.display = 'none';
}

function hideError() {
    elements.errorMessage.style.display = 'none';
}

// ========================================
// FORMATTING HELPERS
// ========================================
function formatCurrency(value) {
    return '€' + parseFloat(value).toFixed(2).replace('.', ',');
}

function formatPercent(value) {
    return parseFloat(value).toFixed(1).replace('.', ',') + '%';
}

// ========================================
// INITIALIZATION
// ========================================
document.addEventListener('DOMContentLoaded', () => {
    // Set initial rates from config
    elements.vsaoi.value = CONFIG.VSAOI_RATE;
    elements.iin.value = CONFIG.IIN_RATE;
    elements.employerVsaoi.value = CONFIG.EMPLOYER_VSAOI_RATE;
    elements.salary.focus();
});