var a = [0,0];
var b = 0;

a[b++] = 1;
console.log(a.toString());
console.log(b);

a[b++]++;
console.log(a.toString());
console.log(b);

var c = {
    d: 5
}

c.d++;
console.log(c.d);
c.d += 1;
console.log(c.d);
