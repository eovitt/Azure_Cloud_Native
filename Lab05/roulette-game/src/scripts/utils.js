function calculateBallTrajectory(angle, speed) {
    const gravity = 9.81; // Acceleration due to gravity
    const time = speed / gravity; // Time of flight
    const x = speed * Math.cos(angle) * time; // Horizontal distance
    const y = speed * Math.sin(angle) * time - (0.5 * gravity * time * time); // Vertical distance
    return { x, y };
}

function detectCollision(ball, wheel) {
    const distance = Math.sqrt((ball.x - wheel.x) ** 2 + (ball.y - wheel.y) ** 2);
    return distance < (ball.radius + wheel.radius);
}

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function degreesToRadians(degrees) {
    return degrees * (Math.PI / 180);
}

function radiansToDegrees(radians) {
    return radians * (180 / Math.PI);
}