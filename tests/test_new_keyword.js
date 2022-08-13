function Car(make, model, year) {
  this.make = make;
  this.model = model;
  this.year = year;
}

const car1 = new Car('Eagle', 'Talon TSi', 1993);
console.log(car1.make);
console.log(Object.getPrototypeOf(car1) == Car.prototype);
