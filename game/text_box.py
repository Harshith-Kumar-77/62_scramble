import pygame
from game.game_logic import valid_letter

class TextBox:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.active = True
        self.font = pygame.font.SysFont(None, 30)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key not in (pygame.K_RETURN, pygame.K_KP_ENTER) and valid_letter(event.unicode) and len(self.text) < 20:
                self.text += event.unicode.upper()

    def clear(self):
        self.text = ""

    def render(self, surface):
        border = (80, 160, 255) if self.active else (100, 105, 115)
        pygame.draw.rect(surface, (250, 250, 252), self.rect, border_radius=7)
        pygame.draw.rect(surface, border, self.rect, width=3, border_radius=7)
        text_surf = self.font.render(self.text, True, (20, 24, 34))
        surface.blit(text_surf, (self.rect.x + 12, self.rect.y + (self.rect.height-text_surf.get_height())//2))
