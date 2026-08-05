
import pygame

from src.constants import SOUND_FILEPATHS

class AudioManager:
    
    def __init__(self):

        # Number of channels that can sound simultaneously
        pygame.mixer.set_num_channels(8)

        self.sounds = {
            k: pygame.mixer.Sound(fp) for k,fp in SOUND_FILEPATHS.items()
            }
        self.mute = False

    def play(self, sound:str):
        if not self.mute:
            self.sounds[sound].play(loops=0, maxtime=0, fade_ms=0)

