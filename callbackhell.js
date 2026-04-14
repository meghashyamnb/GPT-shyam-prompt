//call back hell

function startMachine(callback) { setTimeout(() => { console.log('Machine Started'); callback(); }, 5000); } function grindBeans(callback) { setTimeout(() => { console.log('Grinding coffee beans'); callback(); }, 3000); } function boilWater(callback) { setTimeout(() => { console.log('Boiling Water'); callback(); }, 4000); } function brewCoffee(callback) { setTimeout(() => { console.log('Brewing Coffee'); callback(); }, 3000); } function pourCoffee(callback) { setTimeout(() => { console.log('Pouring coffee into cup'); callback(); }, 2000); }
