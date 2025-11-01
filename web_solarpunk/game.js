// Solarpunk Space - Web Canvas Game
// Collect solar orbs and avoid debris!

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreDisplay = document.getElementById('score');
const restartBtn = document.getElementById('restartBtn');

// Game state
let gameState = {
    player: null,
    orbs: [],
    debris: [],
    stars: [],
    particles: [],
    score: 0,
    gameOver: false,
    spawnTimer: 0,
    debrisTimer: 0,
    keys: {}
};

// Player class
class Player {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.width = 30;
        this.height = 40;
        this.vx = 0;
        this.vy = 0;
        this.speed = 0.5;
        this.drag = 0.95;
        this.maxSpeed = 8;
    }

    update() {
        // Handle input
        if (gameState.keys['ArrowLeft'] || gameState.keys['a']) this.vx -= this.speed;
        if (gameState.keys['ArrowRight'] || gameState.keys['d']) this.vx += this.speed;
        if (gameState.keys['ArrowUp'] || gameState.keys['w']) this.vy -= this.speed;
        if (gameState.keys['ArrowDown'] || gameState.keys['s']) this.vy += this.speed;

        // Apply drag
        this.vx *= this.drag;
        this.vy *= this.drag;

        // Limit speed
        const speed = Math.sqrt(this.vx * this.vx + this.vy * this.vy);
        if (speed > this.maxSpeed) {
            const ratio = this.maxSpeed / speed;
            this.vx *= ratio;
            this.vy *= ratio;
        }

        // Update position
        this.x += this.vx;
        this.y += this.vy;

        // Keep on screen
        this.x = Math.max(this.width / 2, Math.min(canvas.width - this.width / 2, this.x));
        this.y = Math.max(this.height / 2, Math.min(canvas.height - this.height / 2, this.y));
    }

    draw() {
        ctx.save();
        ctx.translate(this.x, this.y);

        // Ship body (mint green)
        ctx.fillStyle = '#64c8b4';
        ctx.beginPath();
        ctx.moveTo(0, -this.height / 2);
        ctx.lineTo(-this.width / 2, this.height / 2);
        ctx.lineTo(this.width / 2, this.height / 2);
        ctx.closePath();
        ctx.fill();

        // Solar core (golden)
        ctx.fillStyle = '#ffd864';
        ctx.beginPath();
        ctx.arc(0, 0, 6, 0, Math.PI * 2);
        ctx.fill();

        ctx.restore();
    }

    getBounds() {
        return {
            x: this.x - this.width / 2,
            y: this.y - this.height / 2,
            width: this.width,
            height: this.height
        };
    }
}

// Solar Orb class
class SolarOrb {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.radius = 10;
        this.floatOffset = Math.random() * Math.PI * 2;
        this.time = 0;
    }

    update() {
        this.time += 0.05;
        this.y += Math.sin(this.time + this.floatOffset) * 0.5;
        this.x -= 1;
    }

    draw() {
        // Outer glow
        const gradient = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.radius * 1.5);
        gradient.addColorStop(0, 'rgba(255, 220, 100, 0.8)');
        gradient.addColorStop(0.5, 'rgba(255, 220, 100, 0.4)');
        gradient.addColorStop(1, 'rgba(255, 220, 100, 0)');
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius * 1.5, 0, Math.PI * 2);
        ctx.fill();

        // Inner orb
        ctx.fillStyle = '#ffd864';
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fill();

        // Highlight
        ctx.fillStyle = '#fff896';
        ctx.beginPath();
        ctx.arc(this.x - 3, this.y - 3, 4, 0, Math.PI * 2);
        ctx.fill();
    }

    getBounds() {
        return {
            x: this.x - this.radius,
            y: this.y - this.radius,
            width: this.radius * 2,
            height: this.radius * 2
        };
    }
}

// Debris class
class Debris {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.size = 30 + Math.random() * 30;
        this.speed = 2 + Math.random() * 2;
        this.rotation = Math.random() * Math.PI * 2;
        this.rotationSpeed = (Math.random() - 0.5) * 0.05;
        this.points = this.generatePoints();
        this.color = `rgb(${180 + Math.random() * 40}, ${130 + Math.random() * 30}, ${90 + Math.random() * 30})`;
    }

    generatePoints() {
        const points = [];
        const numPoints = 6 + Math.floor(Math.random() * 4);
        for (let i = 0; i < numPoints; i++) {
            const angle = (i / numPoints) * Math.PI * 2;
            const radius = this.size / 3 + Math.random() * this.size / 3;
            points.push({
                x: Math.cos(angle) * radius,
                y: Math.sin(angle) * radius
            });
        }
        return points;
    }

    update() {
        this.x -= this.speed;
        this.rotation += this.rotationSpeed;
    }

    draw() {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.rotation);

        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.moveTo(this.points[0].x, this.points[0].y);
        for (let i = 1; i < this.points.length; i++) {
            ctx.lineTo(this.points[i].x, this.points[i].y);
        }
        ctx.closePath();
        ctx.fill();

        ctx.restore();
    }

    getBounds() {
        return {
            x: this.x - this.size / 2,
            y: this.y - this.size / 2,
            width: this.size,
            height: this.size
        };
    }
}

// Star class (background)
class Star {
    constructor(x, y, depth) {
        this.x = x;
        this.y = y;
        this.depth = depth;
        this.speed = 1 / depth;
        this.size = Math.max(1, 3 - depth);
        this.brightness = 150 + depth * 20;
    }

    update() {
        this.x -= this.speed;
        if (this.x < 0) {
            this.x = canvas.width;
            this.y = Math.random() * canvas.height;
        }
    }

    draw() {
        ctx.fillStyle = `rgb(${this.brightness}, ${this.brightness}, ${this.brightness + 30})`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

// Particle class
class Particle {
    constructor(x, y, color, vx, vy) {
        this.x = x;
        this.y = y;
        this.color = color;
        this.vx = vx;
        this.vy = vy;
        this.life = 30;
        this.size = 2 + Math.random() * 3;
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;
        this.life--;
        this.size = Math.max(1, this.size - 0.1);
    }

    draw() {
        const alpha = this.life / 30;
        ctx.fillStyle = this.color.replace('rgb', 'rgba').replace(')', `, ${alpha})`);
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }

    isAlive() {
        return this.life > 0;
    }
}

// Utility functions
function checkCollision(a, b) {
    return a.x < b.x + b.width &&
           a.x + a.width > b.x &&
           a.y < b.y + b.height &&
           a.y + a.height > b.y;
}

function createParticleBurst(x, y, color, count = 10) {
    for (let i = 0; i < count; i++) {
        const angle = Math.random() * Math.PI * 2;
        const speed = 1 + Math.random() * 3;
        const vx = Math.cos(angle) * speed;
        const vy = Math.sin(angle) * speed;
        gameState.particles.push(new Particle(x, y, color, vx, vy));
    }
}

// Initialize game
function initGame() {
    gameState = {
        player: new Player(100, canvas.height / 2),
        orbs: [],
        debris: [],
        stars: [],
        particles: [],
        score: 0,
        gameOver: false,
        spawnTimer: 0,
        debrisTimer: 0,
        keys: {}
    };

    // Create background stars
    for (let i = 0; i < 100; i++) {
        gameState.stars.push(new Star(
            Math.random() * canvas.width,
            Math.random() * canvas.height,
            1 + Math.floor(Math.random() * 3)
        ));
    }

    scoreDisplay.textContent = `Solar Energy: 0`;
    restartBtn.style.display = 'none';
}

// Game loop
function gameLoop() {
    // Clear canvas
    ctx.fillStyle = '#19141f';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Update and draw stars
    gameState.stars.forEach(star => {
        star.update();
        star.draw();
    });

    if (!gameState.gameOver) {
        // Update player
        gameState.player.update();

        // Spawn orbs
        gameState.spawnTimer++;
        if (gameState.spawnTimer > 80 + Math.random() * 70) {
            const y = 50 + Math.random() * (canvas.height - 100);
            gameState.orbs.push(new SolarOrb(canvas.width + 20, y));
            gameState.spawnTimer = 0;
        }

        // Spawn debris
        gameState.debrisTimer++;
        if (gameState.debrisTimer > 60 + Math.random() * 60) {
            const y = 30 + Math.random() * (canvas.height - 60);
            gameState.debris.push(new Debris(canvas.width + 30, y));
            gameState.debrisTimer = 0;
        }

        // Update and draw orbs
        gameState.orbs = gameState.orbs.filter(orb => {
            orb.update();
            orb.draw();

            // Check collision with player
            if (checkCollision(gameState.player.getBounds(), orb.getBounds())) {
                gameState.score += 10;
                scoreDisplay.textContent = `Solar Energy: ${gameState.score}`;
                createParticleBurst(orb.x, orb.y, 'rgb(255, 220, 100)', 15);
                return false;
            }

            return orb.x > -50;
        });

        // Update and draw debris
        gameState.debris = gameState.debris.filter(debris => {
            debris.update();
            debris.draw();

            // Check collision with player
            if (checkCollision(gameState.player.getBounds(), debris.getBounds())) {
                gameState.gameOver = true;
                createParticleBurst(gameState.player.x, gameState.player.y, 'rgb(255, 100, 100)', 30);
                restartBtn.style.display = 'inline-block';
            }

            return debris.x > -100;
        });

        // Update and draw particles
        gameState.particles = gameState.particles.filter(particle => {
            particle.update();
            particle.draw();
            return particle.isAlive();
        });

        // Draw player
        gameState.player.draw();
    } else {
        // Game over - still draw entities and particles
        gameState.orbs.forEach(orb => orb.draw());
        gameState.debris.forEach(debris => debris.draw());
        gameState.particles.forEach(particle => {
            particle.update();
            particle.draw();
        });
        gameState.particles = gameState.particles.filter(p => p.isAlive());

        // Game over text
        ctx.fillStyle = 'rgba(20, 15, 30, 0.7)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = '#ff9696';
        ctx.font = 'bold 48px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('MISSION FAILED', canvas.width / 2, canvas.height / 2 - 40);

        ctx.fillStyle = '#c8ffd8';
        ctx.font = '32px Arial';
        ctx.fillText(`Solar Energy: ${gameState.score}`, canvas.width / 2, canvas.height / 2 + 20);
    }

    requestAnimationFrame(gameLoop);
}

// Input handling
document.addEventListener('keydown', (e) => {
    gameState.keys[e.key] = true;
});

document.addEventListener('keyup', (e) => {
    gameState.keys[e.key] = false;
});

restartBtn.addEventListener('click', initGame);

// Start game
initGame();
gameLoop();
