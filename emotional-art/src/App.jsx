import React, { useState, useEffect, useRef, useCallback } from 'react';
import { findEmotion } from './emotionsConfig';

const EmotionalAlgorithmicArt = () => {
  const [feeling, setFeeling] = useState('');
  const [currentEmotion, setCurrentEmotion] = useState('');
  const [visualParams, setVisualParams] = useState({
    colors: ['#4169E1', '#87CEEB', '#B0E0E6'],
    speed: 0.5,
    rhythm: 'smooth',
    density: 0.5,
    shape: 'circles',
    energy: 0.5
  });
  const canvasRef = useRef(null);
  const animationRef = useRef(null);
  const timeRef = useRef(0);
  const particlesRef = useRef([]);

  // Analyser l'émotion (instantané, sans API)
  const analyzeFeeling = (emotion) => {
    if (!emotion.trim()) return;

    const params = findEmotion(emotion);
    setVisualParams(params);
    setCurrentEmotion(emotion);
  };

  // Initialiser les particules
  const initializeParticles = useCallback((canvas) => {
    const numParticles = Math.floor(visualParams.density * 200);
    particlesRef.current = Array.from({ length: numParticles }, () => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * visualParams.speed * 5,
      vy: (Math.random() - 0.5) * visualParams.speed * 5,
      size: Math.random() * 3 + 1,
      angle: Math.random() * Math.PI * 2,
      angleSpeed: (Math.random() - 0.5) * 0.02,
      life: Math.random(),
      phase: Math.random() * Math.PI * 2,
      bounceVelocity: 0
    }));
  }, [visualParams]);

  // Fonction pour dessiner les différentes formes
  const drawShape = (ctx, particle, shape, size, time, index) => {
    switch (shape) {
      case 'stars':
        ctx.beginPath();
        for (let i = 0; i < 5; i++) {
          const angle = (i * 4 * Math.PI) / 5 - Math.PI / 2;
          const x = Math.cos(angle) * size * 8;
          const y = Math.sin(angle) * size * 8;
          i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.fill();
        break;

      case 'hearts':
        ctx.beginPath();
        const topY = -size * 3;
        ctx.moveTo(0, topY + size * 3);
        ctx.bezierCurveTo(size * 5, topY, size * 8, topY + size * 3, 0, topY + size * 8);
        ctx.bezierCurveTo(-size * 8, topY + size * 3, -size * 5, topY, 0, topY + size * 3);
        ctx.fill();
        break;

      case 'triangles':
        ctx.beginPath();
        ctx.moveTo(0, -size * 8);
        ctx.lineTo(size * 8, size * 8);
        ctx.lineTo(-size * 8, size * 8);
        ctx.closePath();
        ctx.fill();
        break;

      case 'squares':
        ctx.fillRect(-size * 6, -size * 6, size * 12, size * 12);
        break;

      case 'spirals':
        ctx.beginPath();
        for (let i = 0; i < 30; i++) {
          const angle = i * 0.4;
          const radius = i * size * 0.8;
          const x = Math.cos(angle + time) * radius;
          const y = Math.sin(angle + time) * radius;
          i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        }
        ctx.stroke();
        break;

      case 'waves':
        ctx.beginPath();
        ctx.moveTo(-size * 10, 0);
        for (let i = 0; i < 20; i++) {
          const x = -size * 10 + i * size;
          const y = Math.sin(i * 0.5 + time + particle.phase) * size * 3;
          ctx.lineTo(x, y);
        }
        ctx.stroke();
        break;

      case 'lightning':
        ctx.beginPath();
        ctx.moveTo(0, -size * 10);
        let x = 0, y = -size * 10;
        for (let i = 0; i < 5; i++) {
          x += (Math.random() - 0.5) * size * 4;
          y += size * 4;
          ctx.lineTo(x, y);
        }
        ctx.stroke();
        break;

      case 'teardrops':
        ctx.beginPath();
        ctx.arc(0, 0, size * 5, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.moveTo(0, size * 5);
        ctx.bezierCurveTo(size * 3, size * 10, -size * 3, size * 10, 0, size * 5);
        ctx.fill();
        break;

      case 'petals':
        for (let i = 0; i < 6; i++) {
          ctx.save();
          ctx.rotate((i * Math.PI) / 3);
          ctx.beginPath();
          ctx.ellipse(0, size * 5, size * 3, size * 6, 0, 0, Math.PI * 2);
          ctx.fill();
          ctx.restore();
        }
        break;

      case 'shards':
        const sides = 5 + Math.floor(Math.random() * 3);
        ctx.beginPath();
        for (let i = 0; i < sides; i++) {
          const angle = (i * 2 * Math.PI) / sides + time * 0.5;
          const radius = size * (5 + Math.random() * 3);
          const x = Math.cos(angle) * radius;
          const y = Math.sin(angle) * radius;
          i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.fill();
        break;

      case 'arrows':
        ctx.beginPath();
        ctx.moveTo(0, -size * 10);
        ctx.lineTo(0, size * 5);
        ctx.moveTo(0, -size * 10);
        ctx.lineTo(-size * 4, -size * 5);
        ctx.moveTo(0, -size * 10);
        ctx.lineTo(size * 4, -size * 5);
        ctx.stroke();
        break;

      case 'clouds':
        ctx.beginPath();
        ctx.arc(-size * 4, 0, size * 4, 0, Math.PI * 2);
        ctx.arc(0, -size * 2, size * 5, 0, Math.PI * 2);
        ctx.arc(size * 4, 0, size * 4, 0, Math.PI * 2);
        ctx.fill();
        break;

      case 'curves':
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.quadraticCurveTo(
          size * 10,
          size * 5 * Math.sin(time + index),
          size * 20,
          0
        );
        ctx.stroke();
        break;

      case 'lines':
        ctx.beginPath();
        ctx.moveTo(-size * 10, 0);
        ctx.lineTo(size * 10, 0);
        ctx.stroke();
        break;

      default: // circles
        ctx.beginPath();
        ctx.arc(0, 0, size * 5, 0, Math.PI * 2);
        ctx.fill();
    }
  };

  // Animation avec tous les rythmes
  const animate = useCallback((canvas, ctx) => {
    timeRef.current += 0.016 * visualParams.speed;
    const time = timeRef.current;

    ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    particlesRef.current.forEach((particle, index) => {
      // Animation selon le rythme
      switch (visualParams.rhythm) {
        case 'floating':
          particle.x += particle.vx * 0.5;
          particle.y += Math.sin(time + particle.phase) * 2;
          break;

        case 'falling':
          particle.x += particle.vx * 0.3;
          particle.y += visualParams.speed * 3;
          break;

        case 'sinking':
          particle.y += visualParams.speed * 2;
          particle.x += Math.sin(time + particle.phase) * 1;
          break;

        case 'bouncing':
          particle.bounceVelocity += 0.5;
          particle.y += particle.bounceVelocity;
          if (particle.y > canvas.height - 50) {
            particle.y = canvas.height - 50;
            particle.bounceVelocity = -Math.abs(particle.bounceVelocity) * 0.7;
          }
          particle.x += particle.vx;
          break;

        case 'explosive':
          const explosionForce = Math.sin(time * 3) * visualParams.energy * 3;
          particle.x += particle.vx * (1 + explosionForce);
          particle.y += particle.vy * (1 + explosionForce);
          break;

        case 'chaotic':
          particle.x += particle.vx + (Math.random() - 0.5) * visualParams.energy * 4;
          particle.y += particle.vy + (Math.random() - 0.5) * visualParams.energy * 4;
          break;

        case 'trembling':
          particle.x += particle.vx + Math.sin(time * 20 + index) * visualParams.energy * 2;
          particle.y += particle.vy + Math.cos(time * 20 + index) * visualParams.energy * 2;
          break;

        case 'rising':
          particle.x += particle.vx * 0.5;
          particle.y -= visualParams.speed * 2;
          break;

        case 'breathing':
          const breathe = Math.sin(time * 0.5) * visualParams.energy;
          particle.x += particle.vx * (0.5 + breathe);
          particle.y += particle.vy * (0.5 + breathe);
          break;

        case 'pulsing':
          const pulse = Math.sin(time * 2);
          particle.x += particle.vx * (1 + pulse * 0.5);
          particle.y += particle.vy * (1 + pulse * 0.5);
          break;

        case 'erratic':
          particle.x += particle.vx + (Math.random() - 0.5) * visualParams.energy * 2;
          particle.y += particle.vy + (Math.random() - 0.5) * visualParams.energy * 2;
          break;

        case 'focused':
          const centerX = canvas.width / 2;
          const centerY = canvas.height / 2;
          const dx = centerX - particle.x;
          const dy = centerY - particle.y;
          particle.x += particle.vx + dx * 0.001 * visualParams.energy;
          particle.y += particle.vy + dy * 0.001 * visualParams.energy;
          break;

        default: // smooth
          particle.x += particle.vx;
          particle.y += particle.vy;
      }

      // Rebouclage
      if (particle.x < -50) particle.x = canvas.width + 50;
      if (particle.x > canvas.width + 50) particle.x = -50;
      if (particle.y < -50) particle.y = canvas.height + 50;
      if (particle.y > canvas.height + 50) particle.y = -50;

      particle.angle += particle.angleSpeed * visualParams.energy;

      // Dessin
      ctx.save();
      ctx.translate(particle.x, particle.y);
      ctx.rotate(particle.angle);

      const colorIndex = index % visualParams.colors.length;
      const alpha = Math.floor(particle.life * 255).toString(16).padStart(2, '0');
      ctx.fillStyle = visualParams.colors[colorIndex] + alpha;
      ctx.strokeStyle = visualParams.colors[colorIndex];
      ctx.lineWidth = 2;

      drawShape(ctx, particle, visualParams.shape, particle.size, time, index);

      ctx.restore();

      particle.life += 0.01;
      if (particle.life > 1) {
        particle.life = 0;
        particle.x = Math.random() * canvas.width;
        particle.y = Math.random() * canvas.height;
      }
    });

    // Connexions entre particules (optimisé)
    if (visualParams.energy > 0.4) {
      const maxConnections = Math.min(particlesRef.current.length, 50);
      for (let i = 0; i < maxConnections; i++) {
        for (let j = i + 1; j < maxConnections; j++) {
          const p1 = particlesRef.current[i];
          const p2 = particlesRef.current[j];
          const dx = p1.x - p2.x;
          const dy = p1.y - p2.y;
          const distance = Math.sqrt(dx * dx + dy * dy);

          if (distance < 100) {
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            const alpha = (1 - distance / 100) * 0.2 * visualParams.energy;
            ctx.strokeStyle = visualParams.colors[0] + Math.floor(alpha * 255).toString(16).padStart(2, '0');
            ctx.lineWidth = 1;
            ctx.stroke();
          }
        }
      }
    }

    animationRef.current = requestAnimationFrame(() => animate(canvas, ctx));
  }, [visualParams]);

  // Configuration canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      initializeParticles(canvas);
    };

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    animate(canvas, ctx);

    return () => {
      window.removeEventListener('resize', resizeCanvas);
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [animate, initializeParticles]);

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      analyzeFeeling(feeling);
    }
  };

  return (
    <div className="w-full h-screen relative overflow-hidden bg-black">
      <canvas ref={canvasRef} className="absolute inset-0" />

      <div className="absolute top-8 left-8 z-10">
        <h1 className="text-white text-4xl font-light">The feelings machine</h1>
        {currentEmotion && (
          <div className="mt-2">
            <p className="text-white/80 text-lg">Emotion: {currentEmotion}</p>

          </div>
        )}
      </div>

      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 z-10 w-full max-w-2xl px-4">
        <div className="flex gap-2">
          <input
            type="text"
            value={feeling}
            onChange={(e) => setFeeling(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="How are you feeling?"
            className="px-4 py-2 flex-1 rounded-lg bg-black/50 text-white border border-white/30 
                     focus:outline-none focus:border-white/60 backdrop-blur-sm"
          />
          <button
            onClick={() => analyzeFeeling(feeling)}
            className="px-6 py-2 rounded-lg bg-white/10 text-white border border-white/30 
                     transition-colors backdrop-blur-sm hover:bg-white/20"
          >
            Update
          </button>
        </div>

        <div className="mt-4 text-center">
          <p className="text-white/40 text-sm">
            Try: joyful ⭐ sad 💧 furious ⚡ zen 🌊 in love 💕 anxious ⚠️ dreamy ☁️
          </p>
        </div>
      </div>
    </div>
  );
};

export default EmotionalAlgorithmicArt;