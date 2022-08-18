// logical operators test

var a = 7;
var b;
console.log(a || b);
console.log(b || a);
console.log(5 || undefined);
console.log(5 && undefined);
console.log(false && 5)
console.log(5 && false)
console.log(5 && 0)
console.log(0 && false)
console.log(true && 7)
console.log(5 || 10)
console.log(false || 0)

a = 5;
b = 10;
if (a == 5 && b == 10) {
    console.log(1);
}
if (a == 1 && b == 10) {
    console.log(2);
}
if (a == 5 && b == 1) {
    console.log(3);
}
if (a == 1 && b == 1) {
    console.log(4);
}
if (a == 5 || b == 10) {
    console.log(5);
}
if (a == 1 || b == 10) {
    console.log(6);
}
if (a == 5 || b == 1) {
    console.log(7);
}
if (a == 1 || b == 1) {
    console.log(8);
}

