var x = 0;
do {
    x++;
} while (false)

console.log(x);

var y = 0;
do {
    y++;
    if (y == 3) {
        continue;
    }
    console.log(y);
    if (y == 5) {
        break;
    }
} while (true)

