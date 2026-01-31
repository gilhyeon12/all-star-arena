import wave
import math
import struct
import random
import os

SOUND_DIR = "game/sounds"
if not os.path.exists(SOUND_DIR):
    os.makedirs(SOUND_DIR)

FRAMERATE = 44100

def save_wave(filename, data):
    path = os.path.join(SOUND_DIR, filename)
    with wave.open(path, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(FRAMERATE)
        f.writeframes(data)
    print(f"Generated {path}")

def generate_note(freq, duration, volume=0.3, wave_type='square'):
    n_frames = int(FRAMERATE * duration)
    data = bytearray()
    
    for i in range(n_frames):
        t = float(i) / FRAMERATE
        
        # Oscillator
        val = 0
        if wave_type == 'sine':
            val = math.sin(2 * math.pi * freq * t)
        elif wave_type == 'square':
            val = 0.5 if math.sin(2 * math.pi * freq * t) > 0 else -0.5
        elif wave_type == 'saw':
            val = 2.0 * (t * freq - math.floor(t * freq + 0.5))
        elif wave_type == 'noise':
            val = random.uniform(-1, 1)
        elif wave_type == 'triangle':
             val = 2.0 * abs(2.0 * (t * freq - math.floor(t * freq + 0.5))) - 1.0

        # Envelope (ADSR-like simple fade)
        # Attack: fast
        # Decay/Sustain: constant
        # Release: fade out at end
        
        env = 1.0
        if i < 1000: # Attack
            env = i / 1000.0
        elif i > n_frames - 2000: # Release
            env = (n_frames - i) / 2000.0
            
        val = val * volume * env
        
        # 16-bit PCM
        scaled = int(val * 32767)
        data.extend(struct.pack('<h', max(-32768, min(32767, scaled))))
        
    return data

def make_bgm_menu():
    # Simple Arpeggio: C Major
    # C4, E4, G4, C5
    notes = [
        (261.63, 0.2), (329.63, 0.2), (392.00, 0.2), (523.25, 0.4),
        (392.00, 0.2), (329.63, 0.2), (261.63, 0.6)
    ]
    
    full_audio = bytearray()
    # Repeat a few times to make a loopable segment (Pygame loops it anyway)
    for _ in range(2):
        for freq, dur in notes:
            full_audio.extend(generate_note(freq, dur, 0.3, 'square'))
            
    save_wave("bgm_menu.wav", full_audio)

def make_bgm_battle():
    # Excited Battle Theme (Faster, with simulated drums and bass)
    # Tempo: ~150 BPM (0.1s per 16th note approx)
    
    # Melody: A Minor Pentatonic / Blues
    # A3(220), C4(261), D4(293), D#4(311), E4(329), G4(392), A4(440)
    
    # Pattern 1
    melody_notes = [
        (220, 0.2), (220, 0.2), (329, 0.2), (220, 0.2), # A A E A
        (261, 0.2), (293, 0.2), (311, 0.2), (329, 0.2), # C D D# E
        (440, 0.2), (392, 0.2), (329, 0.2), (293, 0.2), # A G E D
        (261, 0.2), (220, 0.2), (196, 0.4)              # C A G(low)
    ]
    
    full_audio = bytearray()
    
    # Generate for loop (repeat melody)
    for _ in range(4): # Loop 4 times
        for freq, dur in melody_notes:
            n_frames = int(FRAMERATE * dur)
            
            # Mix 3 distinct layers: Melody, Bass, Drums
            chunk = bytearray()
            
            for i in range(n_frames):
                t = float(i) / FRAMERATE
                
                # 1. Melody (Square wave, decay volume)
                val_melody = 0.5 if math.sin(2 * math.pi * freq * t) > 0 else -0.5
                env_melody = max(0, 1.0 - (i / n_frames)) # Linear decay
                v1 = val_melody * 0.3 * env_melody
                
                # 2. Bass (Triangle, constant rhythm, lower octave)
                # Play constant 8th notes
                beat_time = t % 0.2 # 0.2s cycle
                bass_freq = 110 # A2
                if freq == 196: bass_freq = 98 # G2 for the G note
                
                val_bass = 2.0 * abs(2.0 * (t * bass_freq - math.floor(t * bass_freq + 0.5))) - 1.0
                env_bass = 1.0 if beat_time < 0.1 else 0.5
                v2 = val_bass * 0.4 * env_bass
                
                # 3. Drums (Noise burst per note start)
                v3 = 0
                if i < 1000: # Kick at start of note
                    v3 = random.uniform(-1, 1) * 0.5
                
                # Mix
                mixed = v1 + v2 + v3
                
                # Clip
                mixed = max(-1.0, min(1.0, mixed))
                
                scaled = int(mixed * 32767)
                chunk.extend(struct.pack('<h', scaled))
                
            full_audio.extend(chunk)
            
    save_wave("bgm_battle.wav", full_audio)

def make_sfx_jump():
    # Rising slide
    duration = 0.3
    n_frames = int(FRAMERATE * duration)
    data = bytearray()
    for i in range(n_frames):
        t = i / FRAMERATE
        # Sweep from 300 to 600
        freq = 300 + (300 * t / duration)
        val = math.sin(2 * math.pi * freq * t)
        val *= (1 - t/duration) # Fade out
        scaled = int(val * 0.4 * 32767)
        data.extend(struct.pack('<h', scaled))
    save_wave("sfx_jump.wav", data)

def make_sfx_attack():
    # White noise burst
    duration = 0.15
    data = bytearray()
    for i in range(int(FRAMERATE * duration)):
        t = i / FRAMERATE
        val = random.uniform(-1, 1)
        val *= (1 - t/duration) ** 2 # Fast fade out
        scaled = int(val * 0.4 * 32767)
        data.extend(struct.pack('<h', scaled))
    save_wave("sfx_attack.wav", data)

def make_sfx_hit():
    # Low frequency square impact
    duration = 0.2
    data = bytearray()
    for i in range(int(FRAMERATE * duration)):
        t = i / FRAMERATE
        freq = 150 - (100 * t / duration) # Pitch drop
        val = 0.5 if math.sin(2 * math.pi * freq * t) > 0 else -0.5
        val *= (1 - t/duration)
        scaled = int(val * 0.5 * 32767)
        data.extend(struct.pack('<h', scaled))
    save_wave("sfx_hit.wav", data)

def make_sfx_select():
    # High ping (Sine)
    duration = 0.1
    data = bytearray()
    for i in range(int(FRAMERATE * duration)):
        t = i / FRAMERATE
        freq = 880 # High A
        val = math.sin(2 * math.pi * freq * t)
        val *= (1 - t/duration)
        scaled = int(val * 0.3 * 32767)
        data.extend(struct.pack('<h', scaled))
    save_wave("sfx_select.wav", data)

if __name__ == "__main__":
    print("Generating sounds...")
    make_bgm_menu()
    make_bgm_battle()
    make_sfx_jump()
    make_sfx_attack()
    make_sfx_hit()
    make_sfx_select()
    print("Done!")
