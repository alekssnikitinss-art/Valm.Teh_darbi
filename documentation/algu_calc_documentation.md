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

## Project Structure

```
algu_calc/
├── index.html        # Main HTML structure and UI
├── app.js           # JavaScript logic and calculations
├── style.css        # Styling and responsive design
└── palaišana        # Server startup script (Latvian: "launch")
```

## File Descriptions

### 1. **index.html**
Main HTML file containing the user interface structure.

**Key Components:**
- **Direction Selector**: Radio buttons to choose calculation direction (Bruto→Neto or Neto→Bruto)
- **Salary Input**: Text field for entering the salary amount in EUR
- **Parameters Section**: Settings for:
  - Tax booklet status (Algas nodokļa grāmatiņa)
  - Number of dependents (Apgādājamo skaits)
  - Tax configuration fields (customizable rates)
  - Deductions toggle

**Output Sections:**
- Results summary showing net and gross salaries
- Detailed deductions breakdown (VSAOI, IIN)
- Employer cost calculations
- Detailed view toggle for additional information

### 2. **app.js**
Core JavaScript file handling all calculations and logic.

**Key Configuration (CONFIG object):**
- `VSAOI_RATE`: 10.5% - Employee social security contribution
- `IIN_RATE`: 20% - Personal income tax
- `EMPLOYER_VSAOI_RATE`: 13.6% - Employer social security contribution
- `NON_TAXABLE_MINIMUM`: €500 - Monthly non-taxable threshold
- `DEPENDENT_DEDUCTION`: €250 - Deduction per dependent

**Main Functions:**
- `handleCalculate()` - Entry point for calculation process
- `calculateBrutoToNeto()` - Converts gross to net salary
- `calculateNetoToBruto()` - Converts net to gross salary
- `validateInput()` - Validates user input
- `displayResults()` - Shows calculation results in UI
- `handleClear()` - Resets all fields

**Features:**
- Real-time calculation on button click or Enter key press
- Error validation and user feedback
- Support for custom tax rates
- Dependent deductions support
- Tax booklet status consideration

### 3. **style.css**
Comprehensive styling with responsive design and animations.

**Design Elements:**
- **Color Scheme**:
  - Primary green gradient (#1B5E20 to #4CAF50)
  - Accent green for highlights (#66BB6A)
  - Error red (#D32F2F)
  - Success green (#388E3C)

- **Layout Features**:
  - Centered calculator box with max-width of 600px
  - Responsive padding and margin spacing
  - Smooth animations and transitions
  - Gradient background overlay
  - Shadow effects for depth

- **Component Styles**:
  - Radio button groups
  - Checkbox groups
  - Input fields with validation states
  - Buttons (primary and secondary)
  - Result display sections
  - Error message styling

### 4. **palaišana**
Server startup script to launch the application locally.

**Command:**
```bash
cd /workspaces/Valm.Teh_darbi/algu_calc && python3 -m http.server 8000
```

**Usage:**
Run this script to start a local HTTP server on port 8000, making the calculator accessible at `http://localhost:8000`

## How to Use

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
