//var randomColour = 0;
var j = 0;

var browserWidth = document.documentElement.clientWidth;

// Origin:
let x = browserWidth / 2;
let y = 400;

var trailLength = 40;
var trailsx = [0];
var trailsy = [0];
var oldx = 0;
var oldy = 0;

let g = 0.6; // gravity - note: 0.6 = ~9.8ms^2
let r1 = 200 ; //length 1
let r2 = 200; // length 2
let m1 = randomNum(40); // mass 1
let m2 = randomNum(40); // mass 2
let a1 = randomNum(360); // angle 1
let a2 = randomNum(360); // angle 2
var a1_v = 0; // angle 1 velocity
var a2_v = 0; // angle 2 velocity

var ctx1 = canvas1.getContext("2d");
var ctx2 = canvas2.getContext("2d");

canvas1.width = browserWidth;
canvas2.width = browserWidth;

function drawLine(x, y, newx, newy, ctx) {
  ctx.beginPath();
  ctx.moveTo(x, y);
  ctx.lineWidth = 5;
  ctx.lineTo(newx, newy);
  ctx.stroke()
}

function drawCircle(x, y, m, ctx, colour) {
  ctx.beginPath();
  ctx.arc(x, y, m, 0, 2 * Math.PI);
  ctx.fillStyle = colour;
  ctx.fill();
  ctx.strokeStyle = colour;
  ctx.stroke()
}

function animate() {

  ctx1.clearRect(0, 0, canvas1.width, canvas1.height);
  //clearCnvs(0,0, canvas1.width, canvas1.height, ctx1);
  //clearCnvs(oldx - 4, oldy - 4, 7.0, 7.0, ctx2);

  // Calc. angle 1's acceleration:
  var nume1 = -g * (2 * m1 + m2) * Math.sin(a1);
  var nume2 = -m2 * g * Math.sin(a1 - 2 * a2);
  var nume3 = -2 * Math.sin(a1 - a2) * m2;
  var nume4 = (a2_v * a2_v *r2) + (a1_v * a1_v * r1) * Math.cos(a1 - a2);
  var denom = r1 * (2 * m1 + m2 - (m2 * Math.cos(2 * a1 - 2 * a2)));

  var a1_a = (nume1 + nume2 + nume3 * nume4) / denom; // angle 1 acceleration

  // Calc. angle 2's acceleration:
  nume1 = 2 * Math.sin(a1 - a2);
  nume2 = a1_v * a1_v * r1 *(m1 + m2);
  nume3 = g * (m1 + m2) * Math.cos(a1);
  nume4 = a2_v * a2_v * r2 * m2 * Math.cos(a1 - a2);
  denom = r2 * (2 * m1 + m2 - (m2 * Math.cos(2 * a1 - 2 * a2)));

  var a2_a = (nume1 * (nume2 + nume3 + nume4)) / denom; // angle 2 acceleration

  // Calc. new position of each ball:
  var x1 = x + (r1 * Math.sin(a1));
  var y1 = y + (r1 * Math.cos(a1));
  var x2 = x1 + (r2 * Math.sin(a2));
  var y2 = y1 + (r2 * Math.cos(a2));

  drawLine(x, y, x1, y1, ctx1);
  drawLine(x1, y1, x2, y2, ctx1);

  drawCircle(x1, y1, m1, ctx1, 'green');
  drawCircle(x2, y2, m2, ctx1, 'green');

  //drawCircle(x1, y1, 2, ctx2, 'red'); // 1st trail
  drawCircle(x2, y2, 2, ctx2, pickColour()); // 2nd trail, with smoothly changing colour

  // Change the velocity, then value
  // of angles based on acceleration
  a1_v += a1_a;
  a2_v += a2_a;
  a1 += a1_v;
  a2 += a2_v;

  // Realistic(?) air resistance:
  //a1_v *= 0.999;
  //a2_v *= 0.999;

  if (trailsx.length >= trailLength) {
    shiftArray(x2, y2);
  } else {
    trailsx.push(x2);
    trailsy.push(y2);
  }

  window.requestAnimationFrame(animate);
}
// End of animate function

function run() {
  console.log("Mass 1: " + m1);
  console.log("Mass 2: " + m2);
  console.log("Length 1: " + r1);
  console.log("Length 2: " + r2);
  console.log("Angle 1: " + a1);
  console.log("Angle 2: " + a2);
  console.log("Gravity: " + g);

  window.requestAnimationFrame(animate);
}

function clearCnvs(x, y, w, h, ctx) {
  ctx.clearRect(x, y, w, h);
}

function shiftArray(x, y) {

  oldx = trailsx[0];
  oldy = trailsy[0];

  for (i = 0; i <= trailsx.length - 1; i++) {
    trailsx[i] = trailsx[i+1]
    trailsy[i] = trailsy[i+1]
  }
  trailsx[trailLength] = x
  trailsy[trailLength] = y
}

function randomNum(x) {
  return num = Math.floor(Math.random() * x);
};

// Generate colour
function pickColour() {
  //randomColour = (Math.cos(j) + 3.6) * 100

  // smooth, oscillating colour:
  j += 1;
  colour = 'hsl(' + j + ', 100%, 50%)';
  return colour
}

// Controls?
function keyDown() {
}

run();
