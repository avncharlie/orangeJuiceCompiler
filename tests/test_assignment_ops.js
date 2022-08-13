// assignment operators test
var a;
var results = [];

a = 10;
a += 2;
results.push(a)

a = 10;
a -= 2;
results.push(a)

a = 10;
a *= 2;
results.push(a)

a = 10;
a /= 2;
results.push(a)

a = 10;
a %= 2;
results.push(a)

a = 10;
a **= 2;
results.push(a)

a = 10;
a <<= 2;
results.push(a)

a = 10;
a >>= 2;
results.push(a)

a = 10;
a >>>= 2;
results.push(a)

a = 10;
a |= 2;
results.push(a)

a = 10;
a ^= 2;
results.push(a)

a = 10;
a &= 2;
results.push(a)

a = 10;
a ||= 2;
results.push(a)

console.log(results.toString())
