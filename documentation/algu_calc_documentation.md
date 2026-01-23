# Algas Kalkulators - Documentation

## Overview

**Algas Kalkulators** (Salary Calculator) is a web-based application designed to calculate employee salaries in Latvia. This calculator helps determine net (take-home) salaries from gross salaries and vice versa, taking into account Latvian tax laws and social security contributions.

## Purpose

The calculator is created for **Valmieras Tehnikums** and serves to:
- Calculate net salary from gross salary (Bruto → Neto)
- Calculate required gross salary from net salary (Neto → Bruto)
- Account for Latvian tax deductions and social security contributions
- Provide detailed breakdowns of deductions and employer costs
- Support customizable tax rates and personal circumstances

---

## JavaScript Fundamentals: Understanding `const`

### What is `const`?

`const` is a JavaScript keyword that declares a **constant variable** - a variable that cannot be reassigned after initialization. It was introduced in ES6 (2015) to provide better code safety and clarity.

**Key characteristics of `const`:**
- **Cannot be reassigned**: Once assigned, the value cannot change
- **Block-scoped**: Only accessible within the block `{}` where it's declared
- **Must be initialized**: You must assign a value when declaring `const`
- **Prevents accidental changes**: Helps catch programming errors

### Why Use `const` in This Project?

In **algu_calc**, `const` is used extensively because:

1. **Configuration Data** - Tax rates shouldn't change during execution
2. **DOM Elements** - References to HTML elements remain constant
3. **Best Practice** - Default to `const`, use `let` only when reassignment is needed
4. **Safety** - Prevents accidental overwrites of important variables

### Comparison: `const` vs `let` vs `var`

| Feature | `const` | `let` | `var` |
|---------|---------|-------|-------|
| Can be reassigned | ❌ No | ✅ Yes | ✅ Yes |
| Block-scoped | ✅ Yes | ✅ Yes | ❌ No (function-scoped) |
| Hoisting | ❌ Temporal Dead Zone | ❌ Temporal Dead Zone | ✅ Yes (undefined) |
| Re-declaration | ❌ No | ❌ No | ✅ Yes |
| Modern JavaScript | ✅ Recommended | ✅ Recommended | ❌ Avoid |

### Example from the Code

```javascript
// Using const for configuration - values that never change
const CONFIG = {
    VSAOI_RATE: 10.5,
    IIN_RATE: 20,
    EMPLOYER_VSAOI_RATE: 13.6,
};

// const salary means we can get the value, but can't reassign it
const salary = parseFloat(elements.salary.value);  // ✅ Correct
salary = 500;  // ❌ Error: Assignment to constant variable
```

---

## Project Structure

```
algu_calc/
├── index.html        # Main HTML structure and UI
├── app.js           # JavaScript logic and calculations
├── style.css        # Styling and responsive design
└── palaišana        # Server startup script (Latvian: "launch")
```

---

## File Descriptions and Code Analysis

### 1. **index.html** - HTML Structure

The HTML file creates the user interface using semantic markup and proper form structure.

#### HTML Structure Overview

```html
<!DOCTYPE html>
<html lang="lv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Algas Kalkulators - Valmieras Tehnikums</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="wrapper">
        <div class="calculator-box">
            <!-- Content goes here -->
        </div>
    </div>
    <script src="app.js"></script>
</body>
</html>
```

**Key HTML Elements:**

#### A) Direction Selector (Calculation Mode)
```html
<div class="direction-selector">
    <label class="radio-group">
        <input type="radio" name="direction" value="bruto-to-neto" checked>
        <span>Bruto → Neto</span>
    </label>
    <label class="radio-group">
        <input type="radio" name="direction" value="neto-to-bruto">
        <span>Neto → Bruto</span>
    </label>
</div>
```
- Radio buttons (only one can be selected at a time)
- `checked` attribute sets default selection to "Bruto → Neto"
- `name="direction"` groups them together

#### B) Salary Input Field
```html
<label for="salary">Alga (EUR):</label>
<input type="number" id="salary" placeholder="Ievadi summu" step="0.01" min="0">
```
- `type="number"` - Ensures numeric input
- `step="0.01"` - Allows two decimal places
- `min="0"` - Prevents negative values
- `id="salary"` - JavaScript will find this element using `document.getElementById('salary')`

#### C) Tax Configuration Section
```html
<label for="vsaoi">VSAOI (%):</label>
<input type="number" id="vsaoi" step="0.1" value="10.5">

<label for="iin">IIN (%):</label>
<input type="number" id="iin" step="0.1" value="20">

<label for="employer-vsaoi">Darba devēja VSAOI (%):</label>
<input type="number" id="employer-vsaoi" step="0.1" value="13.6">
```
- Customizable tax rates with default values
- Users can adjust rates before calculation

#### D) Results Display Section
```html
<div id="results" style="display:none;">
    <div class="results-summary">
        <div class="result-item highlight">
            <span class="label">Neto alga (uz rokas):</span>
            <span class="value" id="netSalary">€0.00</span>
        </div>
        <!-- More result items -->
    </div>
</div>
```
- `display:none` - Hidden by default, shown when calculation completes
- `id="netSalary"` - JavaScript updates this with calculated value

#### E) Detailed Results Table
```html
<table>
    <thead>
        <tr>
            <th>Parametrs</th>
            <th>Procents</th>
            <th>Summa (EUR)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Bruto alga</td>
            <td>100%</td>
            <td id="dt-bruto">€0.00</td>
        </tr>
        <!-- More rows -->
    </tbody>
</table>
```
- HTML table for structured display of detailed calculations
- Each cell has an `id` for JavaScript to update values

---

### 2. **app.js** - JavaScript Logic

The JavaScript file contains all calculation logic, event handling, and DOM manipulation.

#### A) Configuration Object (Using `const`)

```javascript
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
```

**Why `const` here?**
- These tax rates are **fixed values** that should never change
- If someone accidentally tries to modify them, JavaScript will throw an error
- Makes the code safer and clearer

#### B) DOM Elements Object (Using `const`)

```javascript
// ========================================
// DOM ELEMENTS
// ========================================
const elements = {
    // Inputs
    salary: document.getElementById('salary'),
    direction: document.querySelectorAll('input[name="direction"]'),
    vsaoi: document.getElementById('vsaoi'),
    iin: document.getElementById('iin'),
    
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
    // ... more elements
};
```

**Explanation:**
- `document.getElementById()` - Finds HTML element by its `id`
- `document.querySelectorAll()` - Finds multiple elements matching a selector
- Storing in `const elements` object keeps code organized
- Using `elements.salary` instead of `document.getElementById('salary')` is cleaner

**Why store DOM elements?**
- Performance - Only searches DOM once, not repeated searches
- Readability - `elements.salary` is clearer than `document.getElementById('salary')`
- Maintainability - Easier to update if HTML structure changes

#### C) Event Listeners (Adding Interactivity)

```javascript
// ========================================
// EVENT LISTENERS
// ========================================
elements.calculateBtn.addEventListener('click', handleCalculate);
elements.clearBtn.addEventListener('click', handleClear);
elements.salary.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleCalculate();
});
```

**How it works:**
- `addEventListener()` waits for user interaction
- `'click'` - User clicks the button
- `handleCalculate` - Function to run when event occurs
- `'keypress'` with `e.key === 'Enter'` - Allows Enter key to calculate

#### D) Main Calculation Function

```javascript
function handleCalculate() {
    // Clear previous errors
    hideError();
    
    // Get values from HTML elements
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
```

**Step-by-step breakdown:**

1. **Get Values**: `parseFloat()` converts text input to decimal number
   ```javascript
   const salary = parseFloat(elements.salary.value);
   // Example: "1000" → 1000
   ```

2. **Get Direction**: Finds which radio button is checked
   ```javascript
   const direction = Array.from(elements.direction).find(r => r.checked).value;
   // Returns: "bruto-to-neto" or "neto-to-bruto"
   ```

3. **Fallback with `||` (OR operator)**: Uses default if user leaves field empty
   ```javascript
   const vsaoiRate = parseFloat(elements.vsaoi.value) || CONFIG.VSAOI_RATE;
   // If user didn't change it, uses 10.5%
   ```

4. **Validation**: Checks input is valid before calculating
   ```javascript
   const error = validateInput(salary, dependents);
   if (error) {
       showError(error);
       return;  // Stop if error found
   }
   ```

5. **Conditional Calculation**: Different calculation based on direction
   ```javascript
   if (direction === 'bruto-to-neto') {
       result = calculateBrutoToNeto(...);
   } else {
       result = calculateNetoToBruto(...);
   }
   ```

#### E) Bruto to Neto Calculation

```javascript
function calculateBrutoToNeto(bruto, vsaoiRate, iinRate, employerVsaoiRate, dependents, taxBooklet, deductionsEnabled) {
    // Calculate VSAOI deduction
    let vsaoiDeduction = bruto * (vsaoiRate / 100);
    
    // Calculate IIN deduction
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
```

**Mathematical Logic:**

- **VSAOI Calculation**: `bruto × (rate / 100)`
  ```
  Example: 1000 × (10.5 / 100) = 105 EUR
  ```

- **Net Salary**: `bruto - VSAOI - IIN`
  ```
  Example: 1000 - 105 - 200 = 695 EUR (net)
  ```

- **Employer Cost**: `bruto + employer VSAOI`
  ```
  Example: 1000 + (1000 × 0.136) = 1136 EUR total employer cost
  ```

#### F) IIN Tax Calculation

```javascript
function calculateIIN(bruto, vsaoi, iinRate, dependents, taxBooklet, deductionsEnabled) {
    // Base for IIN calculation
    let iinBase = bruto - vsaoi;
    
    // Apply tax booklet deduction if enabled
    let nonTaxableAmount = 0;
    if (taxBooklet && deductionsEnabled) {
        nonTaxableAmount = CONFIG.NON_TAXABLE_MINIMUM;  // 500 EUR
    }
    
    // Apply dependent deductions if enabled
    if (deductionsEnabled) {
        nonTaxableAmount += dependents * CONFIG.DEPENDENT_DEDUCTION;  // 250 EUR per dependent
    }
    
    // Calculate taxable base
    const taxableBase = Math.max(iinBase - nonTaxableAmount, 0);
    
    // Calculate IIN
    const iin = taxableBase * (iinRate / 100);
    
    return iin;
}
```

**Latvian Tax Rules Implemented:**

1. **Start with**: Gross - VSAOI
2. **Subtract minimum**: 500 EUR non-taxable threshold
3. **Subtract dependents**: 250 EUR per dependent
4. **Apply tax rate**: 20% IIN on remaining amount

**Example:**
```
Gross: 1000 EUR
- VSAOI (10.5%): 105 EUR
= IIN Base: 895 EUR
- Non-taxable minimum: 500 EUR
- Dependents (0): 0 EUR
= Taxable base: 395 EUR
× IIN Rate (20%): 79 EUR
```

#### G) Input Validation

```javascript
function validateInput(salary, dependents) {
    if (isNaN(salary) || salary <= 0) {
        return 'Lūdzu, ievadi derīgu summu';  // Please enter valid amount
    }
    
    if (salary > 1000000) {
        return 'Summa pārāk liela. Lūdzu, pārbaudī ievadi.';  // Amount too large
    }
    
    if (dependents < 0 || dependents > 20) {
        return 'Apgādājamo skaits jābūt starp 0 un 20';  // 0-20 dependents
    }
    
    return null;  // No error
}
```

**Validations:**
- `isNaN()` - Checks if value is "Not a Number"
- Salary must be positive
- Salary reasonable (not > 1 million)
- Dependents between 0-20

#### H) Display Results

```javascript
function displayResults(result) {
    // Update summary values
    elements.netSalary.textContent = formatCurrency(result.neto);
    elements.grossSalary.textContent = formatCurrency(result.bruto);
    
    // Update deductions
    elements.vsaoiDeduction.textContent = formatCurrency(result.vsaoiDeduction);
    elements.iinDeduction.textContent = formatCurrency(result.iinDeduction);
    elements.totalDeductions.textContent = formatCurrency(result.totalDeductions);
    
    // Show results section
    elements.results.style.display = 'block';
    elements.results.scrollIntoView({ behavior: 'smooth' });
}
```

**Key operations:**
- `textContent` - Updates HTML element text
- `formatCurrency()` - Converts number to "€X.XX" format
- `style.display = 'block'` - Shows hidden elements
- `scrollIntoView()` - Smoothly scrolls to results

#### I) Format Helpers

```javascript
function formatCurrency(value) {
    return '€' + parseFloat(value).toFixed(2).replace('.', ',');
    // Example: 1000.5 → "€1000,50"
}

function formatPercent(value) {
    return parseFloat(value).toFixed(1).replace('.', ',') + '%';
    // Example: 10.567 → "10,6%"
}
```

**Why replace `.` with `,`?**
- In Latvia, decimals use comma: "1,50 EUR" not "1.50 EUR"
- `.replace('.', ',')` adapts to local format

#### J) Clear Form Function

```javascript
function handleClear() {
    elements.salary.value = '';
    elements.dependents.value = '0';
    elements.taxBooklet.checked = false;
    elements.deductionsEnabled.checked = true;
    elements.detailedView.checked = false;
    elements.results.style.display = 'none';
    elements.errorMessage.style.display = 'none';
    elements.salary.focus();  // Put cursor in salary field
}
```

**Actions:**
- Resets all form inputs to defaults
- Hides results and error messages
- Focuses cursor on salary input field

---

### 3. **style.css** - Visual Design and Layout

CSS provides all styling, animations, and responsive design.

#### A) CSS Variables (Colors)

```css
:root {
    --primary-dark: #1B5E20;      /* Darkest green */
    --primary: #2E7D32;           /* Dark green */
    --primary-light: #4CAF50;     /* Light green */
    --primary-lighter: #81C784;   /* Very light green */
    --accent: #66BB6A;            /* Accent green */
    --text-dark: #1A1A1A;         /* Dark text */
    --text-gray: #424242;         /* Gray text */
    --bg-light: #F1F8F4;          /* Light background */
    --bg-white: #FFFFFF;          /* White background */
    --error: #D32F2F;             /* Error red */
    --success: #388E3C;           /* Success green */
}
```

**Why CSS variables?**
- Change colors globally by updating `:root`
- Makes code more maintainable
- Used with `var(--color-name)`

#### B) Background Gradient

```css
body {
    background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 50%, var(--primary-light) 100%);
    min-height: 100vh;  /* Full viewport height */
}

body::before {
    content: '';
    position: fixed;
    background: linear-gradient(180deg, rgba(255,255,255,0.05) 0%, rgba(27, 94, 32, 0.1) 100%);
    pointer-events: none;  /* Doesn't block clicks */
}
```

**Explanation:**
- `linear-gradient()` - Creates smooth color transition
- `135deg` - Diagonal direction (bottom-left to top-right)
- `rgba()` - Color with transparency
- `::before` - Adds overlay effect over entire page

#### C) Calculator Box Container

```css
.calculator-box {
    background-color: var(--bg-white);
    padding: 3rem 2.5rem;
    border-radius: 16px;
    box-shadow: 0 20px 60px rgba(27, 94, 32, 0.3);
    width: 100%;
    max-width: 600px;
    border-top: 6px solid var(--primary);
    animation: slideIn 0.6s ease-out;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.calculator-box:hover {
    transform: translateY(-8px);
    box-shadow: 0 30px 80px rgba(27, 94, 32, 0.4);
}
```

**Key CSS properties:**
- `border-radius` - Rounded corners
- `box-shadow` - Drop shadow for depth
- `max-width: 600px` - Limits width on large screens
- `animation` - Slide-in effect on load
- `:hover` - Lift effect when mouse hovers

#### D) Input Fields Styling

```css
input[type="number"],
input[type="text"],
select,
textarea {
    width: 100%;
    padding: 0.9rem;
    border: 2px solid var(--accent);
    border-radius: 8px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

input[type="number"]:focus,
input[type="text"]:focus,
select:focus,
textarea:focus {
    outline: none;  /* Remove default blue outline */
    border-color: var(--primary);
    box-shadow: 0 0 0 4px rgba(46, 125, 50, 0.1);
    background-color: rgba(129, 199, 132, 0.05);
}
```

**What happens when user focuses (clicks) input:**
- Border changes to darker green
- Subtle shadow appears
- Background gets light green tint
- Creates visual feedback

#### E) Button Styling

```css
.btn {
    padding: 1.1rem;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    text-transform: uppercase;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 15px rgba(46, 125, 50, 0.3);
}

.btn-primary {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
    color: white;
}

.btn-primary:hover {
    transform: translateY(-3px);  /* Lift up */
    box-shadow: 0 8px 25px rgba(46, 125, 50, 0.4);
}

.btn-primary:active {
    transform: translateY(-1px);  /* Subtle press effect */
}
```

**Button interactions:**
- `:hover` - Lifts button when mouse over
- `:active` - Pressed effect when clicked
- `cursor: pointer` - Changes mouse to hand icon

#### F) Result Display Styling

```css
.result-item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 1rem;
}

.result-item.highlight {
    background: linear-gradient(135deg, rgba(46, 125, 50, 0.1) 0%, rgba(129, 199, 132, 0.1) 100%);
    padding: 1rem;
    border-radius: 6px;
}

.result-item.highlight .value {
    font-weight: 700;
    color: var(--primary);
    font-size: 1.3rem;
}

.deduction-row {
    display: flex;
    justify-content: space-between;
    padding: 0.75rem 0;
    border-bottom: 1px solid rgba(46, 125, 50, 0.1);
}

.deduction-row.total .value {
    font-weight: 700;
    color: var(--primary-dark);
    border-top: 2px solid var(--accent);
}
```

**Layout techniques:**
- `display: flex` - Aligns items horizontally
- `justify-content: space-between` - Spreads items apart
- `border-bottom` - Creates line separators

#### G) Table Styling

```css
table {
    width: 100%;
    border-collapse: collapse;
    background: var(--bg-white);
    box-shadow: 0 2px 8px rgba(46, 125, 50, 0.1);
}

thead {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
    color: white;
}

th, td {
    padding: 1rem;
    text-align: left;
    border-bottom: 1px solid rgba(46, 125, 50, 0.1);
}

tbody tr:hover {
    background-color: var(--bg-light);
}

tbody tr.highlight-row {
    background: linear-gradient(90deg, rgba(46, 125, 50, 0.1) 0%, rgba(129, 199, 132, 0.05) 100%);
    font-weight: 600;
}
```

**Table features:**
- Header has green background with white text
- Rows highlight on hover for better UX
- Important rows get special highlighting

#### H) Responsive Design (Mobile)

```css
@media (max-width: 768px) {
    .wrapper {
        padding: 2rem 1rem;
    }
    
    .calculator-box {
        padding: 2rem 1.5rem;
    }
    
    h1 {
        font-size: 1.8rem;  /* Smaller on mobile */
    }
    
    .direction-selector {
        flex-direction: column;  /* Stack vertically */
        gap: 1rem;
    }
    
    .button-group {
        flex-direction: column;  /* Full-width buttons */
    }
}

@media (max-width: 480px) {
    .calculator-box {
        padding: 1.5rem 1rem;
    }
    
    input[type="number"],
    input[type="text"] {
        font-size: 16px;  /* Prevents zoom on iOS */
    }
}
```

**Mobile optimizations:**
- Reduces padding on small screens
- Stacks elements vertically
- Makes buttons full-width
- Increases input font size to prevent iOS zoom

---

### 4. **palaišana** - Server Startup Script

Simple bash script to launch the application locally.

```bash
cd /workspaces/Valm.Teh_darbi/algu_calc && python3 -m http.server 8000
```

**Breakdown:**
- `cd` - Change directory to algu_calc folder
- `&&` - Run next command only if previous succeeds
- `python3 -m http.server 8000` - Start Python's built-in web server on port 8000

**How to use:**
```bash
./palaišana
# or manually:
python3 -m http.server 8000
```

Then open browser to: `http://localhost:8000`

---

## How to Use the Calculator

1. **Start the Server**:
   ```bash
   ./palaišana
   # or
   python3 -m http.server 8000
   ```

2. **Open in Browser**:
   Navigate to `http://localhost:8000`

3. **Enter Salary Information**:
   - Select calculation direction (Bruto→Neto or Neto→Bruto)
   - Enter salary amount in EUR
   - Configure parameters (tax booklet, dependents, tax rates)
   - Toggle deductions if needed

4. **Calculate**:
   - Click "Aprēķināt" (Calculate) button or press Enter
   - View results including net salary, deductions, and employer costs

5. **Clear**:
   - Click "Notīrīt" (Clear) to reset all fields

---

## Code Flow Diagram

```
User Input
    ↓
[Event Listener] - Click Calculate or Press Enter
    ↓
[handleCalculate()] - Main function
    ↓
[Validate Input] - Check if valid
    ↓
[Choose Direction]
    ├→ Bruto→Neto: [calculateBrutoToNeto()]
    └→ Neto→Bruto: [calculateNetoToBruto()]
    ↓
[Calculate IIN] - Apply tax rules
    ↓
[Return Result Object] - All calculations
    ↓
[displayResults()] - Update HTML
    ↓
[Format with Currency] - "€X.XX"
    ↓
Results Display on Screen
```

---

## Key JavaScript Concepts Used in This Project

### 1. **Objects and Properties**
```javascript
// Objects group related data
const CONFIG = {
    VSAOI_RATE: 10.5,
    IIN_RATE: 20,
};

// Access with dot notation
CONFIG.VSAOI_RATE  // → 10.5
```

### 2. **Functions and Return Values**
```javascript
// Function performs task and returns result
function calculateBrutoToNeto(bruto, vsaoiRate) {
    const vsaoi = bruto * (vsaoiRate / 100);
    return vsaoi;  // Send value back to caller
}

// Use the return value
const deduction = calculateBrutoToNeto(1000, 10.5);  // → 105
```

### 3. **Conditional Logic (if/else)**
```javascript
// Make decisions based on conditions
if (direction === 'bruto-to-neto') {
    result = calculateBrutoToNeto(...);
} else {
    result = calculateNetoToBruto(...);
}
```

### 4. **Loops (for)**
```javascript
// Neto→Bruto uses iteration to find correct bruto
for (let i = 0; i < 100; i++) {
    const result = calculateBrutoToNeto(bruto, ...);
    const diff = result.neto - neto;
    
    if (Math.abs(diff) < 0.01) {
        return result;  // Found answer!
    }
    
    bruto += diff / (1 - (vsaoiRate + iinRate) / 100);
}
```

### 5. **Arrow Functions (Modern JavaScript)**
```javascript
// Short function syntax
elements.salary.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleCalculate();
});
```

### 6. **Template Usage with DOM**
```javascript
// Update HTML with JavaScript values
elements.netSalary.textContent = formatCurrency(result.neto);
// If result.neto = 695, this shows: "€695,00"
```

---

## CSS Concepts Used in This Project

### 1. **CSS Variables (Custom Properties)**
```css
:root {
    --primary-dark: #1B5E20;
}

/* Use anywhere */
color: var(--primary-dark);
```

### 2. **Flexbox Layout**
```css
.result-item {
    display: flex;
    justify-content: space-between;  /* Spread apart */
}
```

Result: Label on left, Value on right

### 3. **Gradients**
```css
background: linear-gradient(135deg, #1B5E20 0%, #4CAF50 100%);
/* Creates smooth color transition */
```

### 4. **Animations and Transitions**
```css
@keyframes slideIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.calculator-box {
    animation: slideIn 0.6s ease-out;
}
```

### 5. **Pseudo-classes (:hover, :focus, :checked)**
```css
input:focus {
    border-color: #2E7D32;  /* Green border when focused */
}

button:hover {
    transform: translateY(-3px);  /* Lift on hover */
}
```

### 6. **Media Queries (Responsive Design)**
```css
@media (max-width: 768px) {
    .button-group {
        flex-direction: column;  /* Stack on mobile */
    }
}
```

---

## Latvian Tax System Integration

### Deductions and Contributions:

1. **VSAOI (Valsts sociālā apdrošināšanas iemaksa)** - Social Security Contribution
   - Employee rate: 10.5%
   - Employer rate: 13.6%

2. **IIN (Iedzīvotāju ienākuma nodoklis)** - Personal Income Tax
   - Standard rate: 20%
   - Affected by non-taxable minimum and dependent deductions

3. **Non-Taxable Minimum**: €500/month
   - Reduces taxable income for IIN calculation

4. **Dependent Deductions**: €250 per dependent
   - Further reduces taxable income

### Tax Booklet (Algas nodokļa grāmatiņa)
When enabled, may provide additional tax relief depending on personal circumstances.

## Features

✅ **Bi-directional Calculation** - Calculate both directions (Bruto↔Neto)  
✅ **Customizable Tax Rates** - Adjust VSAOI, IIN, and employer rates  
✅ **Dependent Support** - Account for family members  
✅ **Tax Booklet Support** - Include tax booklet benefits  
✅ **Detailed Breakdown** - See all deductions and contributions  
✅ **Responsive Design** - Works on desktop and mobile devices  
✅ **Input Validation** - Error handling and user feedback  
✅ **Latvian UI** - Complete Latvian language interface  

## Technical Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Server**: Python HTTP Server
- **Language**: Latvian UI with English code comments
- **Browser Compatibility**: Modern browsers (Chrome, Firefox, Safari, Edge)

## Notes

- All calculations follow Latvian tax legislation
- The calculator provides estimates; official tax calculations may vary
- Tax rates and regulations are current as of the application creation date
- Users should verify significant calculations with official sources

## Related Files

- Main documentation: [database_documentation.md](database_documentation.md)
- Database schema: [FreelancerProjectTrakcer.sql](../DATABASES/FreelancerProjectTrakcer.sql)
- ER Diagram: [ER_Diagram.md](../Diagrams/ER_Diagram.md)
