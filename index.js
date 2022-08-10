/*
// testing 'this'
var obj = {
    outside() {
        return foo();
    },
    insideProp: function() {
        return this;
    },
    insideMember() {
        return this;
    }
}
function foo () {
	return this;
}

console.log(obj.outside() == globalThis);
console.log(obj.insideProp() == obj);
console.log(obj.insideMember() == obj);

/*
function Car(make, model, year) {
  this.make = make;
  this.model = model;
  this.year = year;
}

const car1 = new Car('Eagle', 'Talon TSi', 1993);
console.log(car1.make);
*/

/*
// break and continue nested test on for and while loops
var x = 0;
while (true) {
    x++;
    for (let x=1; x<200; x++) {
        if (x>=20) {
            break;
        }
        if (x % 15 == 0) {
            console.log('FizzBuzz');
            continue;
        }
        if (x % 3 == 0) {
            console.log('Fizz');
        }
        if (x % 5 == 0) {
            console.log('Buzz');
        }
        console.log(x);
    }

    console.log('---------' + x + '---------');

    if (x == 3) {
        break;
    }
}
*/


/*
// fizz buzz
var x = 0;

while (x<20) {
    x += 1;

    if (x % 15 == 0) {
        console.log('FizzBuzz');
        continue;
    }
    if (x % 3 == 0) {
        console.log('Fizz');
    }
    if (x % 5 == 0) {
        console.log('Buzz');
    }
    console.log(x);
}
*/

/*
console.log(a(10));

function a(b) {
    return c(b)+2;
}

function c(b) {
    return b+2;
}
/*



/*
for (let x = 10; x>=0; x--) {
    console.log('yahoo');
}
*/

/*
var x = 0;
while (true) {
    console.log(x);
    if (x == 2){
        break;
    }
    x++;
}
*/

/*
// function demo with factorials and fibonacci

function fact(n) {
	if (n==1) {
  	return 1;
  }
  return n*fact(n-1);
}

function fib(n) {
	if (n < 2) {
  	return 1;
  }
  return fib(n-2) + fib(n-1);
}

console.log('factorials:')
for (let x = 1; x<10; x+=1) {
    console.log(fact(x));
}

console.log('fibonacci:')
for (let x = 1; x<20; x+=1) {
	console.log(fib(x));
}
*/

/*
function a(b) {
    console.log('wow, i got: ' + b + ' as an argument!');
    return b ;
}

a(6);
a('your mother');
a();
*/

// fibonacci
/*
let a = 0;
let b = 1;

for (let count=0; count<3; count+=1) {
    let temp = a+b;
    a = b;
    b = temp;
    console.log(a);
}
*/

// factorial
/*
let fact = 2;
while (fact < 20) {
    let ans = 1;
    for (let x = 2; x < fact; x+=1) {
        ans = ans*x;
    }
    console.log(ans);
    fact += 1;
}
*/

/*
// while loop
var counter = 10;
while (counter != 0) {
    console.log(counter);
    counter -= 1;
}
*/


/*
// scoping example
var a = 5;
console.log('a is: ' + a);
{
    a += 5;
    let a = 1;
    console.log('a is: ' + a);
}
console.log('a is: ' + a);
*/


/*
// functions
function addTwo(num) {
    var x = 2 + num;
}

addTwo(3)    
*/
