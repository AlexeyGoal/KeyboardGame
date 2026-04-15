import pygame
import time

class GameState:
    def __init__(self, word_manager, sound, stats, ui):
        self.word_manager = word_manager
        self.sound = sound
        self.stats = stats
        self.ui = ui
        self.current_level = 0
        self.current_word_index = 0
        self.current_word = ""
        self.time_limit = 0
        self.start_time = 0
        self.remaining_time = 0
        self.user_input = ""
        self.combo = 1
        self.score = 0
        self.restart_timer = 0
        self.state = "PLAYING"  # PLAYING, RESTARTING, LEVEL_COMPLETE, GAME_OVER
        
    def load_level(self, level_idx):
        level = self.word_manager.get_level(level_idx)
        self.words = level["words"]
        self.current_word_index = 0
        self.combo = 1
        self.next_word()
        
    def next_word(self):
        if self.current_word_index >= len(self.words):
            self.state = "LEVEL_COMPLETE"
            return
        self.current_word = self.words[self.current_word_index]
        self.time_limit = self.calculate_timeout(self.current_word)
        self.start_time = time.time()
        self.remaining_time = self.time_limit
        self.user_input = ""
        
    def calculate_timeout(self, word):
        """Расчет времени на слово в зависимости от длины и комбо"""
        base = 1.5
        per_char = 0.3
        length = len(word)
        raw_time = base + (length * per_char)
        # Чем выше комбо, тем меньше времени (усложнение)
        combo_penalty = 1.0 - (self.combo - 1) * 0.05
        combo_penalty = max(0.7, combo_penalty)
        timeout = raw_time * combo_penalty
        return max(1.0, round(timeout, 1))
        
    def handle_input(self, event):
        if self.state != "PLAYING":
            return
            
        if event.key == pygame.K_BACKSPACE:
            self.user_input = self.user_input[:-1]
        elif event.key == pygame.K_RETURN:
            self.check_answer()
        else:
            # Добавляем символ, если это буква
            char = event.unicode
            if char.isalpha() or char.isdigit():
                self.user_input += char
                
    def check_answer(self):
        if self.user_input.strip() == self.current_word:
            # Успех!
            self.sound.play_success()
            points = int(100 * self.combo * (self.remaining_time / self.time_limit))
            self.score += points
            self.combo += 1
            self.current_word_index += 1
            self.stats.record_success(self.current_word)
            self.next_word()
        else:
            # Ошибка
            self.sound.play_fail()
            self.start_restart()
            
    def start_restart(self):
        """Перезапуск уровня из-за ошибки или таймаута"""
        self.state = "RESTARTING"
        self.restart_timer = 3  # 3 секунды до перезапуска
        self.sound.play_timeout()
        self.stats.record_fail(self.current_word)
        
    def update(self, dt):
        if self.state == "PLAYING":
            # Обновляем таймер
            elapsed = time.time() - self.start_time
            self.remaining_time = max(0, self.time_limit - elapsed)
            if self.remaining_time <= 0:
                # Таймаут
                self.start_restart()
                
        elif self.state == "RESTARTING":
            self.restart_timer -= dt
            if self.restart_timer <= 0:
                self.state = "PLAYING"
                self.load_level(self.current_level)
                
        elif self.state == "LEVEL_COMPLETE":
            # Загружаем следующий уровень
            self.current_level += 1
            if self.current_level < self.word_manager.get_level_count():
                self.load_level(self.current_level)
                self.state = "PLAYING"
            else:
                self.state = "GAME_OVER"
                self.stats.save_final_score(self.score)
                
    def draw(self):
        """Отрисовка всего на экране"""
        self.ui.draw_background()
        
        if self.state == "PLAYING":
            # Получаем информацию об уровне для отображения
            level_data = self.word_manager.get_level(self.current_level)
            level_name = level_data["name"]
            total_levels = self.word_manager.get_level_count()
            
            # Отображаем информацию об уровне (простой текст)
            self.ui.draw_level_info(self.current_level, level_name, total_levels)
            
            # Отображаем основные элементы игры
            self.ui.draw_word(self.current_word)
            self.ui.draw_user_input(self.user_input)
            self.ui.draw_timer_bar(self.remaining_time, self.time_limit)
            self.ui.draw_combo(self.combo)
            self.ui.draw_score(self.score)
            
        elif self.state == "RESTARTING":
            # Отображаем сообщение о перезапуске
            self.ui.draw_restart_message(int(self.restart_timer))
            # Также показываем счет и комбо, чтобы игрок не забыл
            self.ui.draw_score(self.score)
            self.ui.draw_combo(self.combo)
            
        elif self.state == "LEVEL_COMPLETE":
            # Отображаем сообщение о завершении уровня
            self.ui.draw_level_complete()
            self.ui.draw_score(self.score)
            
        elif self.state == "GAME_OVER":
            # Отображаем финальный экран
            self.ui.draw_game_over(self.score)