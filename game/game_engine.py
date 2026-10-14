import random
import pygame
from game.text_box import TextBox
from game.game_logic import WORDS, is_correct_guess, normalize_guess, scramble_word, reveal_next_hint, hinted_reward

class GameEngine:
    ROUND_SECONDS = 30.0
    TIMEOUT_FEEDBACK_SECONDS = 1.6

    def __init__(self, width, height):
        self.width, self.height = width, height
        self.words = list(WORDS)
        self.score = 0
        self.feedback_msg = "Unscramble the letters. HINT reveals a letter."
        self.feedback_color = (210, 220, 235)
        self.input_box = TextBox(width // 2 - 165, 286, 220, 44)
        self.submit_btn = pygame.Rect(width // 2 + 65, 286, 105, 44)
        self.hint_btn = pygame.Rect(width // 2 - 165, 350, 105, 38)
        self.restart_btn = pygame.Rect(width // 2 - 45, 350, 115, 38)
        self.font_title = pygame.font.SysFont(None, 42)
        self.font_word = pygame.font.SysFont(None, 46)
        self.font_msg = pygame.font.SysFont(None, 24)
        self.font_small = pygame.font.SysFont(None, 21)
        self.font_btn = pygame.font.SysFont(None, 23)
        self.tile_rects = []
        self.tile_order = []
        self.selected_tile_indices = []
        self.revealed_positions = set()
        self.hints_used = 0
        self.remaining_time = self.ROUND_SECONDS
        self.timeout_pending = 0.0
        self.next_round()

    def next_round(self):
        self.secret_word = random.choice(self.words)
        self.scrambled_word = scramble_word(self.secret_word)
        self.input_box.clear()
        self.revealed_positions = set()
        self.hints_used = 0
        self.remaining_time = self.ROUND_SECONDS
        self.timeout_pending = 0.0
        self.tile_order = list(self.scrambled_word)
        self.selected_tile_indices = []
        random.shuffle(self.tile_order)
        self._layout_tiles()

    def _layout_tiles(self):
        self.tile_rects = []
        tile_w, tile_h, gap = 43, 43, 8
        total = len(self.tile_order) * tile_w + max(0, len(self.tile_order)-1) * gap
        start_x = max(20, (self.width-total)//2)
        y = 205
        for i, _ in enumerate(self.tile_order):
            self.tile_rects.append(pygame.Rect(start_x+i*(tile_w+gap), y, tile_w, tile_h))

    def submit_guess(self, guess=None):
        if self.timeout_pending or self.remaining_time <= 0:
            self.feedback_msg, self.feedback_color = "Time is up. Wait for the next round.", (250, 155, 95)
            return False
        raw = self.input_box.text if guess is None else guess
        value = normalize_guess(raw)
        if not value:
            self.feedback_msg, self.feedback_color = "Type or arrange a word before submitting.", (245, 185, 70)
            return False
        if is_correct_guess(value, self.secret_word):
            earned = hinted_reward(1, self.hints_used)
            self.score += earned
            self.feedback_msg = f"CORRECT! {self.secret_word} — +{earned} point(s)."
            self.feedback_color = (90, 235, 135)
            self.next_round()
            return True
        self.feedback_msg, self.feedback_color = "Not quite — try again. The round has not changed.", (250, 105, 105)
        self.input_box.clear()
        self.selected_tile_indices = []
        return False

    def request_hint(self):
        if self.timeout_pending or self.remaining_time <= 0:
            return
        before = len(self.revealed_positions)
        self.revealed_positions, pattern = reveal_next_hint(self.secret_word, self.revealed_positions)
        if len(self.revealed_positions) > before:
            self.hints_used += 1
            self.feedback_msg = f"Hint ({self.hints_used} used): {pattern}  |  each hint costs 1 point."
            self.feedback_color = (255, 205, 100)
        else:
            self.feedback_msg, self.feedback_color = "All letters have already been revealed.", (255, 205, 100)

    def _restart_game(self):
        self.score = 0
        self.feedback_msg, self.feedback_color = "Game restarted. Good luck!", (210, 220, 235)
        self.next_round()

    def handle_event(self, event):
        # Restart is a global shortcut and must not be typed into the answer box.
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self._restart_game()
            return

        # H triggers a hint when the input is empty or not focused. Once a guess
        # has started, H is typed normally so answers such as PYTHON remain possible.
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_h
                and (not self.input_box.active or not self.input_box.text)):
            self.request_hint()
            return

        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, getattr(pygame, "K_KP_ENTER", pygame.K_RETURN)):
            self.submit_guess()
            return

        self.input_box.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.submit_btn.collidepoint(event.pos):
                self.submit_guess()
            elif self.hint_btn.collidepoint(event.pos):
                self.request_hint()
            elif self.restart_btn.collidepoint(event.pos):
                self._restart_game()
            elif self.input_box.rect.collidepoint(event.pos):
                # Switching to manual typing clears tile-selection bookkeeping,
                # while preserving whatever text is currently in the box.
                self.selected_tile_indices = []
            elif not self.timeout_pending:
                for i, rect in enumerate(self.tile_rects):
                    if rect.collidepoint(event.pos):
                        if i in self.selected_tile_indices:
                            self.selected_tile_indices.remove(i)
                        else:
                            self.selected_tile_indices.append(i)
                        self.input_box.text = "".join(self.tile_order[j] for j in self.selected_tile_indices)
                        self.input_box.active = False
                        break

    def update(self, dt=1/60):
        dt = max(0.0, float(dt))
        if self.timeout_pending:
            self.timeout_pending -= dt
            if self.timeout_pending <= 0:
                self.next_round()
                self.feedback_msg, self.feedback_color = "New round — try the next word!", (210, 220, 235)
            return
        self.remaining_time = max(0.0, self.remaining_time - max(0.0, dt))
        if self.remaining_time <= 0:
            self.feedback_msg = f"TIME! The word was {self.secret_word}. Moving on..."
            self.feedback_color = (250, 155, 95)
            self.timeout_pending = self.TIMEOUT_FEEDBACK_SECONDS

    def _button(self, screen, rect, label, color):
        pygame.draw.rect(screen, color, rect, border_radius=7)
        pygame.draw.rect(screen, (220, 225, 235), rect, width=1, border_radius=7)
        surf = self.font_btn.render(label, True, (255, 255, 255))
        screen.blit(surf, (rect.centerx-surf.get_width()//2, rect.centery-surf.get_height()//2))

    def render(self, screen):
        screen.fill((24, 29, 41))
        title = self.font_title.render("WORD SCRAMBLE ARENA", True, (245, 247, 255))
        screen.blit(title, (self.width//2-title.get_width()//2, 22))
        score = self.font_msg.render(f"Score: {self.score}", True, (255, 221, 105))
        screen.blit(score, (24, 28))
        time_text = self.font_msg.render(f"Time: {self.remaining_time:04.1f}s", True, (255, 221, 105))
        screen.blit(time_text, (self.width-time_text.get_width()-24, 28))
        bar = pygame.Rect(self.width//2-160, 82, 320, 12)
        pygame.draw.rect(screen, (70, 76, 91), bar, border_radius=6)
        fill = pygame.Rect(bar.x, bar.y, int(bar.width*self.remaining_time/self.ROUND_SECONDS), bar.height)
        pygame.draw.rect(screen, (75, 205, 140) if self.remaining_time > 8 else (240, 100, 90), fill, border_radius=6)
        prompt = self.font_small.render("Unscramble the word — click tiles in answer order, or type below", True, (190, 202, 220))
        screen.blit(prompt, (self.width//2-prompt.get_width()//2, 115))
        spaced = "  ".join(self.scrambled_word)
        word_surf = self.font_word.render(spaced, True, (110, 205, 255))
        screen.blit(word_surf, (self.width//2-word_surf.get_width()//2, 145))
        for i, (rect, letter) in enumerate(zip(self.tile_rects, self.tile_order)):
            tile_color = (43, 130, 92) if i in self.selected_tile_indices else (58, 75, 105)
            pygame.draw.rect(screen, tile_color, rect, border_radius=7)
            pygame.draw.rect(screen, (105, 170, 235), rect, width=2, border_radius=7)
            ls = self.font_word.render(letter, True, (255, 255, 255))
            screen.blit(ls, (rect.centerx-ls.get_width()//2, rect.centery-ls.get_height()//2))
        self.input_box.render(screen)
        self._button(screen, self.submit_btn, "SUBMIT", (43, 142, 88))
        self._button(screen, self.hint_btn, "HINT (H)", (145, 105, 40))
        self._button(screen, self.restart_btn, "RESTART (R)", (74, 89, 120))
        msg = self.font_msg.render(self.feedback_msg, True, self.feedback_color)
        screen.blit(msg, (self.width//2-msg.get_width()//2, 410))
        footer = self.font_small.render("Enter = submit  |  H = hint  |  R = restart", True, (145, 157, 179))
        screen.blit(footer, (self.width//2-footer.get_width()//2, self.height-30))
