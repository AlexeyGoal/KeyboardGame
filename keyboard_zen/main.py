import pygame
import sys
from game_state import GameState
from word_manager import WordManager
from ui import UI
from sound import SoundManager
from stats import Stats

class KeyboardZen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Keyboard Zen — Клавиатурный дзен")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 36)
        
        self.sound = SoundManager()
        self.stats = Stats()
        self.word_manager = WordManager()
        self.ui = UI(self.screen, self.font_large, self.font_medium)
        self.game_state = GameState(self.word_manager, self.sound, self.stats, self.ui)
        
        self.running = True
        
    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    else:
                        self.game_state.handle_input(event)
            
            self.game_state.update(dt)
            self.game_state.draw()
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = KeyboardZen()
    game.run()