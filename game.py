import pygame, sys
from pygame.locals import *
import numpy as np
import random
import math

COLOR_WHITE = (255, 255, 255)
COLOR_GRAY = (100, 100, 100)
COLOR_DARK_GRAY = (20, 20, 20)
COLOR_BLACK = (0, 0, 0)
SCREEN_DIMS = [1920, 1080]
MAP_SIZE = [50, 50]
GRID_SIZE = math.floor(min(SCREEN_DIMS) / max(MAP_SIZE))

class Creature:
    def __init__(self, x, y):
        self.health = 100
        self.speed = 1.0
        self.grid_location = [x, y]
        self.pixel_location = [0, 0]

    def render(self, surface):
        pygame.draw.rect(surface,
                         COLOR_WHITE,
                         self.pixel_location + [GRID_SIZE, GRID_SIZE])

    def update(self):
        self.pixel_location = grid.cells[self.grid_location[0]][self.grid_location[1]].pixel_location

class Cell:
    def __init__(self, x, y, w, h):
        self.location = [x, y]
        self.shape = [w, h]
        self.offset = [0, 0]
        self.pixel_location = [0, 0]

    def render(self, surface):
        if self.location == under_mouse:
            color = COLOR_GRAY
        else:
            color = COLOR_DARK_GRAY

        pygame.draw.rect(surface,
                         color,
                         self.pixel_location + [GRID_SIZE, GRID_SIZE],
                         1)

    def update(self):
        self.pixel_location = [
            self.location[0]*GRID_SIZE + self.offset[0],
            self.location[1]*GRID_SIZE + self.offset[1]
        ]
        m = pygame.mouse.get_pos()
        if (not m[0] < self.pixel_location[0]
            and not m[0] > self.pixel_location[0] + GRID_SIZE
            and not m[1] < self.pixel_location[1]
            and not m[1] > self.pixel_location[1] + GRID_SIZE):
            global under_mouse
            under_mouse = self.location

class Grid:
    def __init__(self, x, y, w, h, cell_shape):
        self.cells = [[Cell(i, j, w / cell_shape[0], h / cell_shape[1]) for j in range(cell_shape[0])] for i in range(cell_shape[1])]
        for c in self.cells:
            for c in c:
                c.offset = [x, y]

    def render(self, surface):
        for c in self.cells:
            for c in c:
                c.render(surface)

    def update(self):
        for c in self.cells:
            for c in c:
                c.update()



def randomize_player_locations():
    for p in players:
        p.grid_location = [random.randint(0, MAP_SIZE[0]-1), random.randint(0, MAP_SIZE[1]-1)]


pygame.font.init()
default_font = pygame.font.get_default_font()
font_renderer = pygame.font.Font(default_font, 20)

def draw_text(surface, x, y, text):
    label = font_renderer.render(
        text,   # The font to render
        1,             # With anti aliasing
        (255,255,255)) # RGB Color
    surface.blit(label, (x, y))

def draw_debug_stats(surface):
    draw_text(surface, 10, 10 + 20*0, "fps:" + str(clock.get_fps()))
    draw_text(surface, 10, 10 + 20*1, "mouse:" + str(pygame.mouse.get_pos()))
    draw_text(surface, 10, 10 + 20*2, "under_mouse:" + str(under_mouse))
    draw_text(surface, 10, 10 + 20*3, "selected: n/a")


grid = Grid(SCREEN_DIMS[0]/2 - (MAP_SIZE[0]*GRID_SIZE/2),
            SCREEN_DIMS[1]/2 - (MAP_SIZE[1]*GRID_SIZE/2),
            *SCREEN_DIMS, MAP_SIZE)
players = [
    Creature(random.randint(0, MAP_SIZE[0]-1),random.randint(0, MAP_SIZE[1]-1)) for x in range(10)
]

clock = pygame.time.Clock()
under_mouse = None
selected = None

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = SCREEN_DIMS[0], SCREEN_DIMS[1]

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(SCREEN_DIMS,0,32)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            print(event.unicode)
            if event.unicode == "r":
                randomize_player_locations()
            if event.unicode == "q":
                self._running = False

    def on_loop(self):
        clock.tick(60)
        grid.update()
        for p in players:
            p.update()

    def on_render(self):
        self._display_surf.fill(COLOR_BLACK)
        grid.render(self._display_surf)
        for p in players:
            p.render(self._display_surf)
        draw_debug_stats(self._display_surf)

        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
