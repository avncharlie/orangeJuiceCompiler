var bar = 3;
function f(x) {
    switch (x) {
        case 10:
            console.log('10')
        default:
            console.log('default');
        case 6:
        case 5:
            console.log('5');
        case 4:
            console.log('4');
            while (true) {
                var bar = 10;
                break;
            }
        case 3:
            console.log('3');
            break;
    }
}
f(10);
f(6);
f(5);
f(4);
f(3);
f('foo');
