"""
VIDEO EXPORTER - Génère des vidéos MP4 pour TikTok
Usage: python video_exporter.py

INSTALLATION REQUISE:
pip install opencv-python moviepy numpy pygame
"""

import pygame
import cv2
import numpy as np
import os
import sys

# Importer les fonctions du générateur de patterns
try:
    from pattern_generator import (
        generate_prenom_animation, BG_COLOR, WIDTH, HEIGHT
    )
except ImportError:
    print("\n❌ Erreur: pattern_generator.py doit être dans le même dossier!")
    sys.exit(1)

def generate_video_mp4(prenom, duration=10, fps=60, output_folder="videos"):
    """
    Génère une vidéo MP4 du pattern pour un prénom
    
    Args:
        prenom: Le prénom à animer
        duration: Durée en secondes (défaut: 10s)
        fps: Images par seconde (défaut: 60)
        output_folder: Dossier de sortie
    """
    print(f"\n{'='*60}")
    print(f"🎬 Génération vidéo pour: {prenom}")
    print(f"{'='*60}")
    
    # Initialiser pygame (mode headless)
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.init()
    screen = pygame.Surface((WIDTH, HEIGHT))
    
    # Créer les patterns
    patterns = generate_prenom_animation(prenom)
    
    # Préparer l'export vidéo
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    filename = f"{output_folder}/{prenom}.mp4"
    
    # Codec et writer OpenCV
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, fps, (WIDTH, HEIGHT))
    
    total_frames = duration * fps
    
    print(f"\n⏳ Rendu en cours...")
    print(f"   Frames: {total_frames}")
    print(f"   FPS: {fps}")
    print(f"   Durée: {duration}s")
    print(f"   Résolution: {WIDTH}x{HEIGHT}")
    
    # Barre de progression
    for frame in range(total_frames):
        dt = 1 / fps
        
        # Fond
        screen.fill(BG_COLOR)
        
        # Update et draw tous les patterns
        for pattern in patterns:
            pattern.update(dt)
            pattern.draw(screen)
        
        # Texte du prénom (apparition progressive)
        progress = frame / total_frames
        if progress < 0.2:  # Apparait dans les 2 premières secondes
            alpha = int((progress / 0.2) * 255)
            font = pygame.font.Font(None, 100)
            text = font.render(prenom, True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, 150))
            screen.blit(text, text_rect)
        elif progress > 0.2:
            font = pygame.font.Font(None, 100)
            text = font.render(prenom, True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, 150))
            screen.blit(text, text_rect)
        
        # Convertir pygame surface -> numpy array -> OpenCV
        frame_array = pygame.surfarray.array3d(screen)
        frame_array = np.transpose(frame_array, (1, 0, 2))  # Swap axes
        frame_bgr = cv2.cvtColor(frame_array, cv2.COLOR_RGB2BGR)
        
        # Écrire la frame
        out.write(frame_bgr)
        
        # Barre de progression
        if frame % (fps // 2) == 0:  # Update 2 fois par seconde
            percent = (frame / total_frames) * 100
            bar_length = 40
            filled = int(bar_length * frame / total_frames)
            bar = '█' * filled + '░' * (bar_length - filled)
            print(f"\r   [{bar}] {percent:.1f}%", end='', flush=True)
    
    print(f"\n\n✅ Vidéo créée: {filename}")
    
    # Libérer les ressources
    out.release()
    pygame.quit()
    
    # Taille du fichier
    size_mb = os.path.getsize(filename) / (1024 * 1024)
    print(f"   Taille: {size_mb:.2f} MB")
    
    return filename

def add_music_to_video(video_path, audio_path, output_path=None):
    """
    Ajoute de la musique à une vidéo
    Nécessite moviepy: pip install moviepy
    """
    try:
        from moviepy.editor import VideoFileClip, AudioFileClip
    except ImportError:
        print("\n⚠️  moviepy n'est pas installé!")
        print("Installe-le avec: pip install moviepy")
        return None
    
    print(f"\n🎵 Ajout de la musique...")
    
    if output_path is None:
        base = os.path.splitext(video_path)[0]
        output_path = f"{base}_avec_musique.mp4"
    
    # Charger vidéo et audio
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    
    # Ajuster la durée de l'audio à celle de la vidéo
    audio = audio.subclip(0, min(video.duration, audio.duration))
    
    # Combiner
    final_video = video.set_audio(audio)
    final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')
    
    print(f"✅ Vidéo avec musique: {output_path}")
    
    # Nettoyer
    video.close()
    audio.close()
    final_video.close()
    
    return output_path

def batch_export_videos(prenoms_list, duration=10, fps=60):
    """Exporte plusieurs vidéos d'un coup"""
    print(f"\n{'='*60}")
    print(f"🎬 EXPORT EN BATCH - {len(prenoms_list)} vidéos")
    print(f"{'='*60}")
    
    total_time = len(prenoms_list) * duration * 2  # Estimation pessimiste
    print(f"\n⏱️  Temps estimé: ~{total_time // 60} minutes")
    print(f"💾 Espace requis: ~{len(prenoms_list) * 50} MB\n")
    
    confirm = input("Continuer? (o/n): ").strip().lower()
    if confirm != 'o':
        print("\n❌ Annulé")
        return
    
    videos_created = []
    
    for i, prenom in enumerate(prenoms_list, 1):
        print(f"\n[{i}/{len(prenoms_list)}] {prenom}")
        try:
            video_path = generate_video_mp4(prenom, duration, fps)
            videos_created.append(video_path)
        except Exception as e:
            print(f"❌ Erreur pour {prenom}: {e}")
    
    print(f"\n{'='*60}")
    print(f"✨ Export terminé: {len(videos_created)}/{len(prenoms_list)} vidéos")
    print(f"{'='*60}\n")
    
    return videos_created

def quick_test():
    """Test rapide avec un prénom"""
    print("\n🧪 TEST RAPIDE")
    prenom = input("Entre un prénom: ").strip().upper() or "TEST"
    
    print("\nOptions:")
    print("  1. Vidéo courte (5s, 30fps) - Rapide")
    print("  2. Vidéo standard (10s, 60fps) - Qualité TikTok")
    print("  3. Vidéo haute qualité (15s, 60fps) - Premium")
    
    choice = input("\nChoix (1-3): ").strip()
    
    configs = {
        '1': (5, 30),
        '2': (10, 60),
        '3': (15, 60)
    }
    
    duration, fps = configs.get(choice, (10, 60))
    
    video_path = generate_video_mp4(prenom, duration, fps)
    
    # Proposer d'ajouter de la musique
    print("\n🎵 Veux-tu ajouter de la musique?")
    music_choice = input("Chemin vers un fichier MP3 (ou ENTRÉE pour passer): ").strip()
    
    if music_choice and os.path.exists(music_choice):
        add_music_to_video(video_path, music_choice)
    
    print("\n✅ Test terminé!")

def menu():
    """Menu principal"""
    print("\n" + "="*60)
    print("🎬 VIDEO EXPORTER - Générateur de vidéos TikTok")
    print("="*60)
    print("\nOptions:")
    print("  1. Test rapide (1 vidéo)")
    print("  2. Export batch (prénoms populaires)")
    print("  3. Liste personnalisée")
    print("  4. Ajouter musique à une vidéo existante")
    print("  5. Quitter")
    
    choice = input("\nTon choix (1-5): ").strip()
    
    if choice == "1":
        quick_test()
    
    elif choice == "2":
        from batch_generator import PRENOMS_POPULAIRES
        
        print("\nCombien de prénoms?")
        print("  1. Top 5")
        print("  2. Top 15")
        print("  3. Tous (30)")
        
        sub_choice = input("\nChoix: ").strip()
        
        counts = {'1': 5, '2': 15, '3': 30}
        count = counts.get(sub_choice, 5)
        
        batch_export_videos(PRENOMS_POPULAIRES[:count])
    
    elif choice == "3":
        custom = input("\nPrénoms (séparés par virgules): ")
        prenoms = [p.strip().upper() for p in custom.split(",")]
        batch_export_videos(prenoms)
    
    elif choice == "4":
        video = input("\nChemin vidéo: ").strip()
        music = input("Chemin musique (MP3): ").strip()
        
        if os.path.exists(video) and os.path.exists(music):
            add_music_to_video(video, music)
        else:
            print("\n❌ Fichier(s) introuvable(s)")
    
    elif choice == "5":
        print("\n👋 À bientôt!\n")
        return False
    
    else:
        print("\n❌ Choix invalide")
    
    return True

if __name__ == "__main__":
    # Vérifier les dépendances
    missing = []
    
    try:
        import pygame
    except ImportError:
        missing.append("pygame")
    
    try:
        import cv2
    except ImportError:
        missing.append("opencv-python")
    
    try:
        import numpy
    except ImportError:
        missing.append("numpy")
    
    if missing:
        print("\n❌ Dépendances manquantes:")
        for lib in missing:
            print(f"   - {lib}")
        print(f"\nInstalle-les avec:")
        print(f"   pip install {' '.join(missing)}\n")
        sys.exit(1)
    
    # Lancer le menu
    print("\n✅ Toutes les dépendances sont installées!")
    
    while True:
        if not menu():
            break
        
        input("\nAppuie sur ENTRÉE pour continuer...")