// fibonacci
let a = 0;
let b = 1;

let count='foo';

for (let count=0; count<10; count+=1) {
    let temp = a+b;
    a = b;
    b = temp;
    console.log(a);
}

console.log(count);


