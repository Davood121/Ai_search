/**
 * Holographic Visualization Engine
 * Creates stunning visual effects showing AI's thinking process
 */

class HologramVisualizer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.connections = [];
        this.centerNode = { x: 0, y: 0 };
        this.enginePositions = [];
        this.animationId = null;
        this.state = 'idle'; // idle, breaking, searching, synthesizing

        this.resize();
        window.addEventListener('resize', () => this.resize());
    }

    resize() {
        const rect = this.canvas.parentElement.getBoundingClientRect();
        this.canvas.width = rect.width;
        this.canvas.height = rect.height;
        this.centerNode = {
            x: this.canvas.width / 2,
            y: this.canvas.height / 2
        };
        this.calculateEnginePositions();
    }

    calculateEnginePositions() {
        const radius = Math.min(this.canvas.width, this.canvas.height) * 0.3;
        const engines = 5;
        this.enginePositions = [];

        for (let i = 0; i < engines; i++) {
            const angle = (i / engines) * Math.PI * 2 - Math.PI / 2;
            this.enginePositions.push({
                x: this.centerNode.x + Math.cos(angle) * radius,
                y: this.centerNode.y + Math.sin(angle) * radius
            });
        }
    }

    start(state = 'searching') {
        this.state = state;
        if (this.animationId) return;
        this.animate();
    }

    stop() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }
    }

    clear() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.particles = [];
        this.connections = [];
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Draw based on current state
        this.drawCenterNode();
        this.drawConnections();
        this.updateParticles();
        this.drawParticles();

        if (this.state === 'searching') {
            this.spawnParticles();
        }

        this.animationId = requestAnimationFrame(() => this.animate());
    }

    drawCenterNode() {
        const { x, y } = this.centerNode;
        const time = Date.now() / 1000;

        // Pulsating center node
        const pulseSize = 15 + Math.sin(time * 2) * 5;

        // Outer glow
        const gradient = this.ctx.createRadialGradient(x, y, 0, x, y, pulseSize * 3);
        gradient.addColorStop(0, 'rgba(0, 217, 255, 0.3)');
        gradient.addColorStop(1, 'rgba(0, 217, 255, 0)');
        this.ctx.fillStyle = gradient;
        this.ctx.beginPath();
        this.ctx.arc(x, y, pulseSize * 3, 0, Math.PI * 2);
        this.ctx.fill();

        // Core
        this.ctx.fillStyle = '#00D9FF';
        this.ctx.beginPath();
        this.ctx.arc(x, y, pulseSize, 0, Math.PI * 2);
        this.ctx.fill();

        // Inner glow
        this.ctx.fillStyle = '#FFFFFF';
        this.ctx.beginPath();
        this.ctx.arc(x, y, pulseSize * 0.5, 0, Math.PI * 2);
        this.ctx.fill();
    }

    drawConnections() {
        const time = Date.now() / 1000;

        this.enginePositions.forEach((pos, index) => {
            // Animated connection lines
            const progress = (Math.sin(time * 2 + index) + 1) / 2;

            // Gradient line
            const gradient = this.ctx.createLinearGradient(
                this.centerNode.x,
                this.centerNode.y,
                pos.x,
                pos.y
            );

            const colors = [
                'rgba(0, 217, 255, 0.6)',  // SearXNG
                'rgba(255, 149, 0, 0.6)',  // DuckDuckGo
                'rgba(157, 78, 221, 0.6)', // Qwant
                'rgba(255, 255, 255, 0.6)',// Wikipedia
                'rgba(76, 175, 80, 0.6)'   // Wikidata
            ];

            gradient.addColorStop(0, colors[index]);
            gradient.addColorStop(progress, colors[index]);
            gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');

            this.ctx.strokeStyle = gradient;
            this.ctx.lineWidth = 2;
            this.ctx.beginPath();
            this.ctx.moveTo(this.centerNode.x, this.centerNode.y);

            // Calculate intermediate point for curve
            const midX = (this.centerNode.x + pos.x) / 2;
            const midY = (this.centerNode.y + pos.y) / 2;
            const offset = Math.sin(time + index) * 20;

            this.ctx.quadraticCurveTo(
                midX + offset,
                midY - offset,
                pos.x,
                pos.y
            );
            this.ctx.stroke();
        });
    }

    spawnParticles() {
        if (Math.random() < 0.3) {
            // Spawn from random engine
            const engineIndex = Math.floor(Math.random() * this.enginePositions.length);
            const startPos = this.enginePositions[engineIndex];

            this.particles.push({
                x: startPos.x,
                y: startPos.y,
                targetX: this.centerNode.x,
                targetY: this.centerNode.y,
                progress: 0,
                speed: 0.01 + Math.random() * 0.02,
                size: 2 + Math.random() * 3,
                color: this.getEngineColor(engineIndex),
                alpha: 1
            });
        }
    }

    getEngineColor(index) {
        const colors = [
            '#00D9FF',  // SearXNG - Cyan
            '#FF9500',  // DuckDuckGo - Orange
            '#9D4EDD',  // Qwant - Purple
            '#FFFFFF',  // Wikipedia - White
            '#4CAF50'   // Wikidata - Green
        ];
        return colors[index] || '#FFFFFF';
    }

    updateParticles() {
        this.particles = this.particles.filter(particle => {
            particle.progress += particle.speed;

            if (particle.progress >= 1) {
                return false; // Remove particle
            }

            // Ease-in-out interpolation
            const t = particle.progress;
            const ease = t < 0.5
                ? 2 * t * t
                : -1 + (4 - 2 * t) * t;

            particle.x = particle.x + (particle.targetX - particle.x) * particle.speed * 2;
            particle.y = particle.y + (particle.targetY - particle.y) * particle.speed * 2;
            particle.alpha = 1 - ease;

            return true;
        });
    }

    drawParticles() {
        this.particles.forEach(particle => {
            this.ctx.save();
            this.ctx.globalAlpha = particle.alpha;

            // Glow effect
            const gradient = this.ctx.createRadialGradient(
                particle.x, particle.y, 0,
                particle.x, particle.y, particle.size * 3
            );
            gradient.addColorStop(0, particle.color);
            gradient.addColorStop(1, 'transparent');

            this.ctx.fillStyle = gradient;
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.size * 3, 0, Math.PI * 2);
            this.ctx.fill();

            // Core
            this.ctx.fillStyle = particle.color;
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            this.ctx.fill();

            this.ctx.restore();
        });
    }

    // Trigger explosion effect when synthesis completes
    triggerSynthesisEffect() {
        const { x, y } = this.centerNode;

        // Create radial burst of particles
        for (let i = 0; i < 30; i++) {
            const angle = (i / 30) * Math.PI * 2;
            const distance = 100 + Math.random() * 100;

            this.particles.push({
                x: x,
                y: y,
                targetX: x + Math.cos(angle) * distance,
                targetY: y + Math.sin(angle) * distance,
                progress: 0,
                speed: 0.02,
                size: 3,
                color: '#9D4EDD',
                alpha: 1
            });
        }
    }
}
