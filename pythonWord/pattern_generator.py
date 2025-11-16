"""
PREMIUM PATTERN GENERATOR - Version "WOAH" 🔥
Effets visuels next level pour TikTok

Installation:
pip install pygame numpy
"""

import pygame
import math
import numpy as np
import random
from pygame import gfxdraw

# Initialisation
pygame.init()
WIDTH, HEIGHT = 1080, 1920  # Format TikTok
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Premium Pattern Generator - WOAH Mode")
clock = pygame.time.Clock()

# Couleurs premium
BG_COLOR = (255, 255, 255)
PREMIUM_COLORS = [
    (255, 50, 150),   # Rose néon
    (50, 200, 255),   # Cyan électrique
    (150, 255, 50),   # Vert lime
    (255, 150, 50),   # Orange vif
    (200, 50, 255),   # Violet néon
    (255, 255, 50),   # Jaune électrique
    (50, 255, 200),   # Turquoise
]

class ParticleSystem:
    """Système de particules massif avec physique"""
    def __init__(self, x, y, color, num_particles=500):
        self.particles = []
        self.color = color
        
        # Créer des particules avec vélocités aléatoires
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 200)
            self.particles.append({
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': random.uniform(0.5, 2.0),
                'max_life': random.uniform(0.5, 2.0),
                'size': random.uniform(2, 6)
            })
    
    def update(self, dt):
        for p in self.particles[:]:
            # Physique
            p['x'] += p['vx'] * dt
            p['y'] += p['vy'] * dt
            p['vy'] += 100 * dt  # Gravité
            p['vx'] *= 0.99  # Friction
            p['life'] -= dt
            
            if p['life'] <= 0:
                self.particles.remove(p)
    
    def draw(self, surface):
        for p in self.particles:
            alpha = int(255 * (p['life'] / p['max_life']))
            if alpha > 0 and 0 <= p['x'] < WIDTH and 0 <= p['y'] < HEIGHT:
                # Glow effect - dessiner plusieurs fois avec alpha décroissant
                for i in range(3):
                    glow_size = int(p['size'] + i * 2)
                    glow_alpha = max(0, alpha - i * 80)
                    color = (*self.color, glow_alpha)
                    
                    try:
                        # Effet de glow
                        gfxdraw.filled_circle(surface, int(p['x']), int(p['y']), 
                                            glow_size, (*self.color, glow_alpha // 3))
                        # Particule centrale
                        if i == 0:
                            gfxdraw.filled_circle(surface, int(p['x']), int(p['y']), 
                                                int(p['size']), self.color)
                    except:
                        pass

class GlowingSpiral:
    """Spirale avec effets de lumière et traînées"""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.time = 0
        self.trail_points = []
        
    def update(self, dt):
        self.time += dt
        
    def draw(self, surface):
        num_points = 200
        max_radius = 350 + math.sin(self.time * 2) * 80
        
        points = []
        for i in range(num_points):
            t = i / num_points
            angle = t * 8 * math.pi + self.time
            radius = t * max_radius
            
            # Distorsion ondulante
            wave = math.sin(self.time * 3 + t * 10) * 20
            radius += wave
            
            x = int(self.x + radius * math.cos(angle))
            y = int(self.y + radius * math.sin(angle))
            points.append((x, y))
        
        # Dessiner avec glow effect
        for i, (x, y) in enumerate(points):
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                alpha = 255 - int((i / num_points) * 180)
                size = int(12 - (i / num_points) * 8)
                
                # Glow layers
                for layer in range(4):
                    glow_size = size + layer * 3
                    glow_alpha = max(0, alpha - layer * 60)
                    
                    try:
                        # Outer glow
                        gfxdraw.filled_circle(surface, x, y, glow_size, 
                                            (*self.color, glow_alpha // 4))
                        # Core
                        if layer == 0:
                            gfxdraw.filled_circle(surface, x, y, size, self.color)
                            gfxdraw.aacircle(surface, x, y, size, (255, 255, 255))
                    except:
                        pass

class MorphingShape:
    """Forme qui se transforme avec effets 3D"""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.time = 0
        
    def update(self, dt):
        self.time += dt
        
    def draw(self, surface):
        num_vertices = 6
        base_radius = 200
        
        for layer in range(15, 0, -1):
            # Chaque layer tourne à une vitesse différente
            rotation = self.time * (1 + layer * 0.1)
            scale = layer / 15
            
            points = []
            for i in range(num_vertices):
                angle = (i / num_vertices) * 2 * math.pi + rotation
                
                # Distorsion dynamique
                radius = base_radius * scale
                radius += math.sin(self.time * 2 + i) * 30 * scale
                
                # Effet 3D - perspective
                z = math.sin(self.time + layer * 0.2) * 50
                perspective = 1 / (1 + z / 1000)
                
                x = int(self.x + radius * math.cos(angle) * perspective)
                y = int(self.y + radius * math.sin(angle) * perspective)
                points.append((x, y))
            
            # Dessiner avec alpha pour effet de profondeur
            alpha = int(50 + layer * 10)
            
            # Gradient color based on layer
            layer_color = tuple(int(c * (0.5 + scale * 0.5)) for c in self.color)
            
            try:
                if len(points) >= 3:
                    # Glow effect autour du polygone
                    for glow in range(3):
                        glow_points = []
                        for px, py in points:
                            offset = glow * 5
                            # Expand polygon
                            dx = px - self.x
                            dy = py - self.y
                            dist = math.sqrt(dx*dx + dy*dy)
                            if dist > 0:
                                glow_points.append((
                                    int(px + (dx/dist) * offset),
                                    int(py + (dy/dist) * offset)
                                ))
                        
                        if len(glow_points) >= 3:
                            pygame.draw.polygon(surface, (*layer_color, alpha // (glow + 1)), 
                                              glow_points, max(1, 3 - glow))
                    
                    # Core shape
                    pygame.draw.polygon(surface, layer_color, points)
                    pygame.draw.polygon(surface, (255, 255, 255), points, 2)
            except:
                pass

class WaveDistortion:
    """Vagues de distorsion avec effets ripple"""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.time = 0
        
    def update(self, dt):
        self.time += dt
        
    def draw(self, surface):
        num_circles = 25
        
        for i in range(num_circles):
            # Multiple waves avec des vitesses différentes
            offset1 = (self.time * 150 + i * 40) % 600
            offset2 = (self.time * 100 + i * 30) % 500
            
            radius = 30 + (offset1 + offset2) / 2
            
            if radius < 450:
                # Pulsation alpha
                pulse = abs(math.sin(self.time * 3 + i * 0.5))
                alpha = int(200 * pulse * (1 - radius / 450))
                
                # Thickness varie
                thickness = int(3 + pulse * 4)
                
                # Dessiner plusieurs cercles pour effet de glow
                for glow in range(3):
                    glow_radius = int(radius + glow * 2)
                    glow_thickness = max(1, thickness - glow)
                    glow_alpha = max(0, alpha - glow * 60)
                    
                    try:
                        # Outer glow
                        pygame.draw.circle(surface, (*self.color, glow_alpha // 3),
                                         (int(self.x), int(self.y)), 
                                         glow_radius, glow_thickness + 2)
                        # Core ring
                        if glow == 0:
                            pygame.draw.circle(surface, self.color,
                                             (int(self.x), int(self.y)), 
                                             int(radius), thickness)
                    except:
                        pass

class EnergyField:
    """Champ d'énergie avec particules interconnectées"""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.time = 0
        self.nodes = []
        
        # Créer des nodes
        for i in range(12):
            angle = (i / 12) * 2 * math.pi
            self.nodes.append({
                'base_angle': angle,
                'base_dist': 150,
                'phase': random.uniform(0, 2 * math.pi)
            })
        
    def update(self, dt):
        self.time += dt
        
    def draw(self, surface):
        # Calculer positions des nodes
        positions = []
        for node in self.nodes:
            angle = node['base_angle'] + self.time * 0.5
            dist = node['base_dist'] + math.sin(self.time * 2 + node['phase']) * 50
            
            x = self.x + dist * math.cos(angle)
            y = self.y + dist * math.sin(angle)
            positions.append((x, y))
        
        # Dessiner connexions
        for i, (x1, y1) in enumerate(positions):
            for j in range(i + 1, len(positions)):
                x2, y2 = positions[j]
                
                # Distance pour alpha
                dx = x2 - x1
                dy = y2 - y1
                dist = math.sqrt(dx*dx + dy*dy)
                
                if dist < 250:
                    alpha = int(255 * (1 - dist / 250))
                    
                    # Dessiner ligne avec glow
                    try:
                        # Glow lines
                        for glow in range(3):
                            line_alpha = max(0, alpha - glow * 80)
                            thickness = max(1, 3 - glow)
                            pygame.draw.line(surface, (*self.color, line_alpha // 2),
                                           (int(x1), int(y1)), (int(x2), int(y2)), 
                                           thickness)
                    except:
                        pass
        
        # Dessiner nodes
        for x, y in positions:
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                # Glow effect
                for glow in range(4):
                    glow_size = 8 + glow * 3
                    glow_alpha = 255 - glow * 60
                    
                    try:
                        gfxdraw.filled_circle(surface, int(x), int(y), glow_size,
                                            (*self.color, glow_alpha // 3))
                        if glow == 0:
                            gfxdraw.filled_circle(surface, int(x), int(y), 8, self.color)
                            gfxdraw.aacircle(surface, int(x), int(y), 8, (255, 255, 255))
                    except:
                        pass

class ExplosiveFlower:
    """Fleur explosive avec pétales animés"""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.time = 0
        
    def update(self, dt):
        self.time += dt
        
    def draw(self, surface):
        num_petals = 12
        
        for petal in range(num_petals):
            angle = (petal / num_petals) * 2 * math.pi + self.time * 0.3
            
            # Pulsation
            pulse = abs(math.sin(self.time * 3 + petal * 0.5))
            length = 150 + pulse * 100
            
            # Points du pétale (bezier-like)
            points = []
            for i in range(15):
                t = i / 14
                
                # Courbe du pétale
                curve = math.sin(t * math.pi) * 0.5
                dist = length * t
                
                # Rotation
                petal_angle = angle + curve * 0.3
                
                x = int(self.x + dist * math.cos(petal_angle))
                y = int(self.y + dist * math.sin(petal_angle))
                points.append((x, y))
            
            # Dessiner pétale avec gradient
            for i in range(len(points) - 1):
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                
                alpha = int(255 * (1 - i / len(points)) * pulse)
                thickness = max(1, int(8 * (1 - i / len(points))))
                
                # Glow
                for glow in range(2):
                    glow_thickness = thickness + glow * 2
                    glow_alpha = max(0, alpha - glow * 100)
                    
                    try:
                        pygame.draw.line(surface, (*self.color, glow_alpha // 2),
                                       (x1, y1), (x2, y2), glow_thickness)
                    except:
                        pass
                
                # Core line
                try:
                    pygame.draw.line(surface, self.color, (x1, y1), (x2, y2), thickness)
                except:
                    pass
        
        # Centre lumineux
        for glow in range(6):
            glow_size = 20 + glow * 5
            glow_alpha = 255 - glow * 40
            
            try:
                gfxdraw.filled_circle(surface, int(self.x), int(self.y), glow_size,
                                    (*self.color, glow_alpha // 2))
                if glow == 0:
                    gfxdraw.filled_circle(surface, int(self.x), int(self.y), 20, 
                                        (255, 255, 255))
            except:
                pass

def get_premium_pattern_for_letter(letter, color, x, y):
    """Assigne un pattern premium à chaque lettre"""
    patterns = {
        'A': GlowingSpiral, 'N': GlowingSpiral,
        'B': WaveDistortion, 'O': WaveDistortion,
        'C': MorphingShape, 'P': MorphingShape,
        'D': ExplosiveFlower, 'Q': ExplosiveFlower,
        'E': EnergyField, 'R': EnergyField,
        'F': GlowingSpiral, 'S': WaveDistortion,
        'G': MorphingShape, 'T': ExplosiveFlower,
        'H': EnergyField, 'U': GlowingSpiral,
        'I': WaveDistortion, 'V': MorphingShape,
        'J': ExplosiveFlower, 'W': EnergyField,
        'K': GlowingSpiral, 'X': WaveDistortion,
        'L': MorphingShape, 'Y': ExplosiveFlower,
        'M': ExplosiveFlower, 'Z': EnergyField,
    }
    
    letter = letter.upper()
    PatternClass = patterns.get(letter, GlowingSpiral)
    return PatternClass(x, y, color)

def generate_premium_animation(text):
    """Génère l'animation premium"""
    text = text.upper()
    patterns = []
    particle_systems = []
    
    # Introduction avec explosion de particules
    for i, letter in enumerate(text):
        color = PREMIUM_COLORS[i % len(PREMIUM_COLORS)]
        
        # Position
        if len(text) <= 4:
            x = WIDTH // 2
            y = HEIGHT // 2 - 300 + i * 150
        else:
            angle = (i / len(text)) * 2 * math.pi - math.pi / 2
            radius = 350
            x = WIDTH // 2 + radius * math.cos(angle)
            y = HEIGHT // 2 + radius * math.sin(angle)
        
        pattern = get_premium_pattern_for_letter(letter, color, x, y)
        patterns.append(pattern)
        
        # Ajouter particules pour l'intro
        if i < 3:  # Juste pour les premières lettres (sinon trop lourd)
            particle_systems.append(ParticleSystem(x, y, color, num_particles=300))
    
    return patterns, particle_systems

def draw_text_with_glow(surface, text, size, x, y, color=(255, 255, 255)):
    """Texte avec effet de glow"""
    font = pygame.font.Font(None, size)
    
    # Glow layers
    for glow in range(5):
        glow_size = size + glow * 2
        glow_font = pygame.font.Font(None, glow_size)
        glow_alpha = 255 - glow * 50
        
        text_surface = glow_font.render(text, True, (*color, glow_alpha // 3))
        text_surface.set_alpha(glow_alpha // 3)
        text_rect = text_surface.get_rect(center=(x, y))
        surface.blit(text_surface, text_rect)
    
    # Core text
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

def main():
    print("\n🔥 PREMIUM PATTERN GENERATOR - WOAH MODE")
    print("=" * 60)
    text = input("Entre un texte (prénom, mot, etc.): ").strip()
    
    if not text:
        text = "FIRE"
    
    print(f"\n✨ Génération PREMIUM pour: {text}")
    print("⚠️  Effets visuels intenses!")
    print("\nControles:")
    print("  ESPACE = Pause")
    print("  R = Régénérer")
    print("  ESC = Quitter\n")
    
    patterns, particle_systems = generate_premium_animation(text)
    
    running = True
    paused = False
    start_time = pygame.time.get_ticks()
    
    # Surface avec alpha pour effets de glow
    glow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    while running:
        dt = clock.tick(60) / 1000.0
        current_time = (pygame.time.get_ticks() - start_time) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_r:
                    patterns, particle_systems = generate_premium_animation(text)
                    start_time = pygame.time.get_ticks()
        
        if not paused:
            # Background avec gradient subtil
            screen.fill(BG_COLOR)
            
            # Vignette effect
            for i in range(10):
                alpha = int(30 * (i / 10))
                margin = i * 20
                try:
                    rect = pygame.Rect(margin, margin, 
                                     WIDTH - margin * 2, HEIGHT - margin * 2)
                    pygame.draw.rect(screen, (*BG_COLOR, alpha), rect, 2)
                except:
                    pass
            
            # Clear glow surface
            glow_surface.fill((0, 0, 0, 0))
            
            # Update et draw patterns sur glow surface
            for pattern in patterns:
                pattern.update(dt)
                pattern.draw(glow_surface)
            
            # Update et draw particle systems
            for ps in particle_systems[:]:
                ps.update(dt)
                ps.draw(glow_surface)
                
                # Nettoyer les systèmes vides
                if len(ps.particles) == 0 and current_time > 3:
                    particle_systems.remove(ps)
            
            # Blit glow surface
            screen.blit(glow_surface, (0, 0))
            
            # Texte avec glow (apparition progressive)
            if current_time < 2:
                alpha = int((current_time / 2) * 255)
                draw_text_with_glow(screen, text, 120, WIDTH // 2, 200, 
                                   (255, 255, 255))
            elif current_time < 8:
                draw_text_with_glow(screen, text, 120, WIDTH // 2, 200, 
                                   (255, 255, 255))
            else:
                # Fade out
                alpha = int(255 * (1 - (current_time - 8) / 2))
                if alpha > 0:
                    draw_text_with_glow(screen, text, 120, WIDTH // 2, 200, 
                                       (255, 255, 255))
            
            pygame.display.flip()
            
            # Boucler après 10 secondes
            if current_time > 10:
                patterns, particle_systems = generate_premium_animation(text)
                start_time = pygame.time.get_ticks()
        else:
            draw_text_with_glow(screen, "PAUSE", 100, WIDTH // 2, HEIGHT // 2,
                              (255, 100, 100))
            pygame.display.flip()
    
    pygame.quit()
    print("\n✅ Terminé!")
    print("\n💡 NEXT LEVEL:")
    print("- Ajoute de la musique épique")
    print("- Exporte en 60 FPS pour du slow-mo")
    print("- Combine plusieurs effets")
    print("- Teste avec des mots courts: FIRE, LOVE, VIBE\n")

if __name__ == "__main__":
    main()