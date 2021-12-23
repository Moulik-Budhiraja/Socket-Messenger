import pygame
import socket
from client import Client
pygame.font.init()

WIDTH, HEIGHT = 800, 600

FPS = 60

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREY = (100, 100, 100)

messages = []


class Button:
    FONT = pygame.font.SysFont('Arial', 20)

    def __init__(self, screen: pygame.Surface, text: str, x: int, y: int, width: int, height: int, color: tuple) -> None:
        self.screen = screen
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.text = Button.FONT.render(self.text, True, (0, 0, 0))

    def draw(self) -> None:
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.screen, self.color, self.hitbox)
        self.screen.blit(self.text, (self.x + self.width // 2 - self.text.get_width() //
                         2, self.y + self.height // 2 - self.text.get_height() // 2))

    def is_clicked(self, mouse_pos: tuple) -> bool:
        return self.hitbox.collidepoint(mouse_pos)


class TextBox:
    FONT = pygame.font.SysFont('Arial', 20)

    def __init__(self, screen: pygame.Surface, text: str, x: int, y: int, width: int, height: int, color: tuple, active=False) -> None:
        self.screen = screen
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.original_width = width
        self.height = height
        self.color = color * active or GREY
        self.original_color = color
        self.active = active

        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rendered_text = TextBox.FONT.render(self.text, True, WHITE)

        self.backspace = False
        self.backspace_time = 0

    def draw(self) -> None:
        pygame.draw.rect(self.screen, self.color, self.hitbox, 2)
        self.screen.blit(self.rendered_text, (self.x + 10, self.y +
                         self.height // 2 - self.rendered_text.get_height() // 2))

    def is_clicked(self, mouse_pos: tuple) -> bool:
        return self.hitbox.collidepoint(mouse_pos)

    def set_focus(self, focus: bool) -> None:
        if focus:
            self.color = self.original_color
            self.active = True
        else:
            self.color = GREY
            self.active = False

    def update_text(self, event: pygame.event) -> None:
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.backspace = True
                elif event.key == pygame.K_RETURN:
                    self.backspace = False
                    self.backspace_time = 0
                else:
                    self.text += event.unicode

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    self.backspace = False
                    self.backspace_time = 0

    def update_backspace(self) -> None:
        if self.backspace and self.active:

            if self.backspace_time == 0:
                self.text = self.text[:-1]
            elif self.backspace_time > 15 and self.backspace_time % 2 == 0:
                self.text = self.text[:-1]

            self.backspace_time += 1

    def update(self, max_width) -> None:
        self.rendered_text = TextBox.FONT.render(self.text, True, WHITE)
        self.width = max(self.original_width,
                         self.rendered_text.get_width() + 20)
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

        if self.width + self.x > max_width:
            self.text = self.text[:-1]
            self.update(max_width)


class Gui:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chat')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 20)

        # OBJECTS
        self.name_box = TextBox(
            self.screen, '', 600, 50, 100, 50, BLUE)
        self.text_box = TextBox(self.screen, '', 100, 500, 200, 50, BLUE)
        self.send_button = Button(
            self.screen, 'Send', 300, 500, 100, 50, GREEN)

    def render(self) -> None:
        self.screen.fill((128, 128, 128))

        self.name_box.draw()
        self.text_box.draw()
        self.send_button.draw()

        pygame.display.update()
        self.clock.tick(FPS)


def main() -> None:
    client.connect()
    gui = Gui()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                client.disconnect(author=gui.name_box.text)
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if gui.text_box.is_clicked(event.pos):
                    gui.text_box.set_focus(True)
                else:
                    gui.text_box.set_focus(False)

                if gui.name_box.is_clicked(event.pos):
                    gui.name_box.set_focus(True)
                else:
                    gui.name_box.set_focus(False)

                if gui.send_button.is_clicked(event.pos):
                    client.send(author=gui.name_box.text,
                                msg=gui.text_box.text)
                    gui.text_box.text = ''

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if gui.text_box.active:
                        client.send(author=gui.name_box.text,
                                    msg=gui.text_box.text)
                        gui.text_box.text = ''

            gui.name_box.update_text(event)
            gui.text_box.update_text(event)

        gui.name_box.update_backspace()
        gui.name_box.update(max_width=700)
        gui.text_box.update_backspace()
        gui.text_box.update(max_width=600)

        gui.send_button.x, gui.send_button.y = gui.text_box.x + \
            gui.text_box.width, gui.text_box.y

        gui.render()


client = Client(socket.gethostbyname(socket.gethostname()))
main()
