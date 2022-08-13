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


