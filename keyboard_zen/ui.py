import pygame

class UI:
    def __init__(self, screen, font_large, font_medium):
        self.screen = screen
        self.font_large = font_large
        self.font_medium = font_medium
        self.width, self.height = screen.get_size()
        
    def draw_background(self):
        self.screen.fill((30, 30, 40)) 
        
    def draw_word(self, word):
        text = self.font_large.render(word, True, (255, 255, 255))
        x = self.width // 2 - text.get_width() // 2
        y = self.height // 3
        self.screen.blit(text, (x, y))
        
    def draw_user_input(self, user_input):
        text = self.font_large.render(user_input + "_", True, (200, 200, 100))
        x = self.width // 2 - text.get_width() // 2
        y = self.height // 2
        self.screen.blit(text, (x, y))
        
    def draw_timer_bar(self, remaining, total):
        ratio = remaining / total if total > 0 else 0
        bar_width = 400
        bar_height = 20
        x = self.width // 2 - bar_width // 2
        y = self.height - 100
        
        pygame.draw.rect(self.screen, (100, 100, 100), (x, y, bar_width, bar_height))
        
        if ratio > 0.5:
            color = (0, 255, 0) 
        elif ratio > 0.2:
            color = (255, 255, 0)  
        else:
            color = (255, 0, 0)  
        pygame.draw.rect(self.screen, color, (x, y, int(bar_width * ratio), bar_height))
        
    def draw_combo(self, combo):
        if combo > 1:
            text = self.font_medium.render(f"Комбо x{combo}!", True, (255, 200, 0))
            x = self.width - 150
            y = 20
            self.screen.blit(text, (x, y))
            
    def draw_score(self, score):
        text = self.font_medium.render(f"Очки: {score}", True, (255, 255, 255))
        self.screen.blit(text, (20, 20))
        
    def draw_restart_message(self, seconds):
        text = self.font_large.render(f"Уровень перезапускается... {seconds}", True, (255, 100, 100))
        x = self.width // 2 - text.get_width() // 2
        y = self.height // 2
        self.screen.blit(text, (x, y))
        
    def draw_level_complete(self):
        text = self.font_large.render("Уровень пройден!", True, (100, 255, 100))
        x = self.width // 2 - text.get_width() // 2
        y = self.height // 2
        self.screen.blit(text, (x, y))
        
    def draw_game_over(self, score):
        self.screen.fill((0, 0, 0))
        text1 = self.font_large.render("Игра пройдена!", True, (255, 255, 255))
        text2 = self.font_medium.render(f"Финальный счет: {score}", True, (200, 200, 200))
        text3 = self.font_medium.render("Нажмите ESC для выхода", True, (150, 150, 150))
        x1 = self.width // 2 - text1.get_width() // 2
        x2 = self.width // 2 - text2.get_width() // 2
        x3 = self.width // 2 - text3.get_width() // 2
        self.screen.blit(text1, (x1, self.height // 3))
        self.screen.blit(text2, (x2, self.height // 2))
        self.screen.blit(text3, (x3, self.height // 2 + 50))

    def draw_level_info(self, level_number, level_name, total_levels):
        """Отображает информацию о текущем уровне"""
        text = self.font_medium.render(f"Уровень {level_number + 1}/{total_levels}: {level_name}", True, (200, 200, 200))
        x = self.width // 2 - text.get_width() // 2
        y = 20
        self.screen.blit(text, (x, y))