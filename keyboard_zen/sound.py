import pygame
import os

class SoundManager:
    def __init__(self, assets_folder="assets"):
        self.assets_folder = assets_folder
        self.success_sound = self.load_sound("success.wav")
        self.fail_sound = self.load_sound("fail.wav")
        self.timeout_sound = self.load_sound("timeout.wav")
        self.bonus_sound = self.load_sound("bonus.wav")
        
    def load_sound(self, filename):
        path = os.path.join(self.assets_folder, filename)
        if os.path.exists(path):
            return pygame.mixer.Sound(path)
        return None
        
    def play_success(self):
        if self.success_sound:
            self.success_sound.play()
            
    def play_fail(self):
        if self.fail_sound:
            self.fail_sound.play()
            
    def play_timeout(self):
        if self.timeout_sound:
            self.timeout_sound.play()
            
    def play_bonus(self):
        if self.bonus_sound:
            self.bonus_sound.play()