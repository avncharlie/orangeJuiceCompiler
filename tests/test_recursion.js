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
