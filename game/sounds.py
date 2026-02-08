import pygame
import os

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music_playing = None
        self.enabled = True
        
        # Initialize mixer with specific settings for lower latency
        if not pygame.mixer.get_init():
            try:
                # frequency, size, channels, buffer
                pygame.mixer.init(44100, -16, 2, 512)
            except Exception as e:
                print(f"Failed to init mixer: {e}")
                self.enabled = False
                return

        self.load_sounds()
    
    def load_sounds(self):
        if not self.enabled: return
        
        sound_dir = "game/sounds"
        sound_files = {
            "jump": "sfx_jump.wav",
            "attack": "sfx_attack.wav",
            "hit": "sfx_hit.wav",
            "select": "sfx_select.wav",
            "dash": "sfx_jump.wav", # Reuse for dash
            "block": "sfx_select.wav", # Placeholder for block/poof
            "rasengan": "sfx_attack.wav", # Placeholder for energy skill
            "clone": "sfx_jump.wav" # Placeholder for clone poof
        }
        
        for name, filename in sound_files.items():
            path = os.path.join(sound_dir, filename)
            if os.path.exists(path):
                try:
                    sound = pygame.mixer.Sound(path)
                    sound.set_volume(0.5) # Default volume
                    self.sounds[name] = sound
                    print(f"Loaded sound: {name}")
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
            else:
                print(f"Sound file not found: {path}")
                
        # Music files (streamed separately)
        self.music_files = {
            "menu": os.path.join(sound_dir, "bgm_menu.wav"),
            "battle": os.path.join(sound_dir, "bgm_battle.wav")
        }

    def play_sfx(self, name):
        if not self.enabled: return
        if name in self.sounds:
            self.sounds[name].play()
            
    def play_bgm(self, name, loop=-1):
        if not self.enabled: return
        if name not in self.music_files: return
        if self.music_playing == name: return # Already playing
        
        path = self.music_files[name]
        self._load_and_play(path, name, loop)

    def play_custom_bgm(self, path, loop=-1):
        """특정 경로의 BGM 재생 (BGM Hijacking용)"""
        if not self.enabled: return
        if not os.path.exists(path):
            print(f"Custom BGM missing: {path}")
            return
        
        self._load_and_play(path, "custom", loop)

    def _load_and_play(self, path, name_tag, loop):
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(loop)
            self.music_playing = name_tag
            print(f"Playing BGM: {path}")
        except Exception as e:
            print(f"Error playing music {path}: {e}")
            
    def stop_bgm(self):
        if not self.enabled: return
        pygame.mixer.music.stop()
        self.music_playing = None
    
    def set_bgm_volume(self, volume_percent):
        # volume_percent: 0-100
        if not self.enabled: return
        vol = max(0.0, min(1.0, volume_percent / 100.0))
        pygame.mixer.music.set_volume(vol)

    def set_sfx_volume(self, volume_percent):
        # volume_percent: 0-100
        if not self.enabled: return
        vol = max(0.0, min(1.0, volume_percent / 100.0))
        for s in self.sounds.values():
            s.set_volume(vol)
