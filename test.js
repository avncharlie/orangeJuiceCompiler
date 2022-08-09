
let fact = 1;
while (fact < 10) {
    let ans = 1;
    for (let x = 2; x < fact; x+=1) {
        ans = ans*x;
    }
    console.log(ans);
    fact += 1;
}


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
