var queue = {
    link: {
        link: {
            link: null
        }
    }
}

let peek = 5, next = queue;
while ((peek = next.link) != null) {
    next = peek;
    console.log(peek);
}
next.link = 5;

console.log('---');
console.log(queue);

