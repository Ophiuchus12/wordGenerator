"""
BATCH GENERATOR - Génère automatiquement plusieurs patterns
Usage: python batch_generator.py
"""

import pygame
import math
import os
from pattern_generator import (
    generate_prenom_animation, BG_COLOR, WIDTH, HEIGHT
)

# Liste des prénoms populaires français (2024)
PRENOMS_POPULAIRES = [
    # Filles
    "EMMA", "JADE", "LOUISE", "ALICE", "CHLOE", "LINA", "MIA", "LEA",
    "ROSE", "ANNA", "JULIA", "ZOE", "ELENA", "SARAH", "LUNA",
    
    # Garçons  
    "GABRIEL", "RAPHAEL", "LEO", "LOUIS", "ARTHUR", "NOAH", "LIAM",
    "LUCAS", "HUGO", "NATHAN", "ADAM", "JULES", "TOM", "THEO", "PAUL",
]

def generate_single_prenom_preview(prenom, output_folder="outputs"):
    """
    Génère une image preview du pattern pour un prénom
    (plus rapide qu'une vidéo pour tester)
    """
    pygame.init()
    screen = pygame.Surface((WIDTH, HEIGHT))
    
    patterns = generate_prenom_animation(prenom)
    
    # Rendre 5 secondes d'animation
    for frame in range(300):  # 5s à 60fps
        dt = 1/60
        
        screen.fill(BG_COLOR)
        
        for pattern in patterns:
            pattern.update(dt)
            pattern.draw(screen)
        
        # Texte du prénom
        font = pygame.font.Font(None, 100)
        text = font.render(prenom, True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, 150))
        screen.blit(text, text_rect)
    
    # Sauvegarder la dernière frame
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    filename = f"{output_folder}/{prenom}_preview.png"
    pygame.image.save(screen, filename)
    pygame.quit()
    
    return filename

def generate_batch_previews(prenoms_list=None):
    """Génère des previews pour une liste de prénoms"""
    if prenoms_list is None:
        prenoms_list = PRENOMS_POPULAIRES[:5]  # Top 5 par défaut
    
    print("\n" + "="*60)
    print("🎨 BATCH GENERATOR - Génération de previews")
    print("="*60)
    
    for i, prenom in enumerate(prenoms_list, 1):
        print(f"\n[{i}/{len(prenoms_list)}] Génération: {prenom}...", end=" ")
        
        try:
            filename = generate_single_prenom_preview(prenom)
            print(f"✅ Créé: {filename}")
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    print("\n" + "="*60)
    print(f"✨ {len(prenoms_list)} previews générées!")
    print("="*60)
    print("\n💡 PROCHAINE ÉTAPE:")
    print("Installe opencv-python et moviepy pour générer des vidéos:")
    print("  pip install opencv-python moviepy")
    print("\nPuis utilise video_exporter.py pour créer des MP4\n")

def show_stats(prenoms_list=None):
    """Affiche des stats sur les patterns"""
    if prenoms_list is None:
        prenoms_list = PRENOMS_POPULAIRES
    
    from collections import Counter
    
    print("\n" + "="*60)
    print("📊 STATISTIQUES DES PATTERNS")
    print("="*60)
    
    # Compter les lettres
    all_letters = "".join(prenoms_list)
    letter_count = Counter(all_letters)
    
    print(f"\n📝 Total de prénoms: {len(prenoms_list)}")
    print(f"🔤 Total de lettres: {len(all_letters)}")
    print(f"\n🏆 Top 5 lettres les plus utilisées:")
    
    for letter, count in letter_count.most_common(5):
        print(f"   {letter}: {count} fois")
    
    # Longueurs de prénoms
    lengths = [len(p) for p in prenoms_list]
    avg_length = sum(lengths) / len(lengths)
    
    print(f"\n📏 Longueur moyenne: {avg_length:.1f} lettres")
    print(f"   Plus court: {min(lengths)} lettres")
    print(f"   Plus long: {max(lengths)} lettres")
    
    print("\n" + "="*60 + "\n")

def menu():
    """Menu interactif"""
    print("\n" + "="*60)
    print("🎨 GÉNÉRATEUR DE PATTERNS TIKTOK - BATCH MODE")
    print("="*60)
    print("\nOptions:")
    print("  1. Générer Top 5 prénoms populaires")
    print("  2. Générer Top 15 prénoms populaires")
    print("  3. Générer TOUS les prénoms (30 prénoms)")
    print("  4. Entrer une liste personnalisée")
    print("  5. Voir les statistiques")
    print("  6. Quitter")
    
    choice = input("\nTon choix (1-6): ").strip()
    
    if choice == "1":
        generate_batch_previews(PRENOMS_POPULAIRES[:5])
    elif choice == "2":
        generate_batch_previews(PRENOMS_POPULAIRES[:15])
    elif choice == "3":
        print("\n⚠️  Attention: cela va prendre ~5 minutes")
        confirm = input("Continuer? (o/n): ").strip().lower()
        if confirm == 'o':
            generate_batch_previews(PRENOMS_POPULAIRES)
    elif choice == "4":
        custom = input("\nEntre les prénoms séparés par des virgules: ")
        prenoms = [p.strip().upper() for p in custom.split(",")]
        generate_batch_previews(prenoms)
    elif choice == "5":
        show_stats()
    elif choice == "6":
        print("\n👋 À bientôt!\n")
        return False
    else:
        print("\n❌ Choix invalide")
    
    return True

if __name__ == "__main__":
    # Vérifier que pygame est installé
    try:
        import pygame
    except ImportError:
        print("\n❌ Pygame n'est pas installé!")
        print("Installe-le avec: pip install pygame\n")
        exit(1)
    
    # Boucle du menu
    while True:
        if not menu():
            break
        
        input("\nAppuie sur ENTRÉE pour continuer...")