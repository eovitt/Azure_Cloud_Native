const canvas = document.getElementById('rouletteCanvas');
const ctx = canvas.getContext('2d');

let angle = 0;
let speed = 0.1;
let ballRadius = 10;
let ballAngle = 0;
let ballSpeed = 0.2;
let ballBouncing = true;

function drawRouletteWheel() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.save();
    ctx.translate(canvas.width / 2, canvas.height / 2);
    ctx.rotate(angle);
    
    // Draw the wheel
    ctx.fillStyle = '#ff0000';
    ctx.beginPath();
    ctx.arc(0, 0, 150, 0, Math.PI * 2);
    ctx.fill();
    
    // Draw the ball
    if (ballBouncing) {
        ballAngle += ballSpeed;
        let ballX = 150 * Math.cos(ballAngle);
        let ballY = 150 * Math.sin(ballAngle);
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(ballX, ballY, ballRadius, 0, Math.PI * 2);
        ctx.fill();
    }
    
    ctx.restore();
}

function update() {
    angle += speed;
    drawRouletteWheel();
    requestAnimationFrame(update);
}

function startGame() {
    speed = 0.1; // Set initial speed
    ballBouncing = true; // Start the ball bouncing
    update();
}

function stopGame() {
    speed = 0; // Stop the wheel
    ballBouncing = false; // Stop the ball
}

// Start the game when the page loads
window.onload = startGame;