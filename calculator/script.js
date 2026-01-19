// Alert paziņojums
function showAlert() {
    alert("Poga tika nospiesta!");
    console.log("Alert poga nospiesta");
}

// Teksta maiņa + stila maiņa
function changeText() {
    const textElement = document.getElementById("mainText");
    textElement.innerHTML = "Teksts ir veiksmīgi nomainīts!";
    textElement.style.color = "red";
    console.log("Teksts nomainīts");
}

// Kalkulators
function calculate() {
    const number1 = Number(document.getElementById("num1").value);
    const number2 = Number(document.getElementById("num2").value);

    let sum = number1 + number2;
    document.getElementById("result").innerHTML = sum;

    console.log("Aprēķinātā summa:", sum);
}

// Sveiciena funkcija ar prompt
function greetUser() {
    const name = prompt("Ievadi savu vārdu:");
    if (name) {
        alert("Sveiki, " + name + "!");
        console.log("Lietotājs:", name);
    }
}
