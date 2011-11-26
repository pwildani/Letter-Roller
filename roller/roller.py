import itertools
import pygame
import random
import sys
import time
import string

# Abbreviate UI constants.
from pygame.locals import *

try:
    import android
except ImportError:
    android = None

# TODO adapt to the device
WINDOWWIDTH = 480
WINDOWHEIGHT = 800

# Will attempt no more than this FPS.
FPS = 15

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHTCYAN = (0, 100, 255)
BLUE = (0, 153, 153)
GREEN = (0, 204, 0)

BGCOLOR = BLUE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = LIGHTCYAN

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE


class Board:
  def __init__(self, rows, cols):
    self.rows = rows
    self.cols = cols

  def letterAt(self, row, col):
    # TODO real code
    return string.letters[row + col * self.cols].upper()


class TermBoardUI:
   def __init__(self, board):
     self.board = board

   def draw(self):
     for r in range(self.board.rows):
       print
       for c in range(self.board.cols):
         print self.board.letterAt(r, c),
     print


class PyGameBoardUI:
  def __init__(self, surface, board, gap):
    self.surface = surface
    self.board = board
    self.rows = board.rows
    self.cols = board.cols

    rect = surface.get_rect()
    self.width = rect.width
    self.height = rect.height


    self.bordersize = 3
    self.gap = gap
    self.xmargin = gap + self.bordersize
    self.ymargin = gap + self.bordersize

    fitwidth = (self.width - gap - self.bordersize) / self.cols
    fitheight = (self.height - gap - self.bordersize) / self.rows
    self.tilesize = min(fitwidth, fitheight)

    self.fontsize = self.tilesize / 2
    self.font = pygame.font.Font('freesansbold.ttf', self.fontsize)

  def draw(self):
    self.surface.fill(BGCOLOR)

    # Render the letters
    for r in range(self.rows):
      for c in range(self.cols):
        self.drawCell(r, c, self.board.letterAt(r, c))

    # Render a box around the letters
    top, left = self.getTopLeftOfTile(0, 0)
    width = self.cols * self.tilesize + self.cols * self.gap
    height = self.rows * self.tilesize + self.rows * self.gap
    pygame.draw.rect(self.surface, BORDERCOLOR,  (
        left - self.bordersize, top - self.bordersize,
        width + self.bordersize, height + self.bordersize),
      self.bordersize)

  def drawCell(self, row, col, label):
    top, left = self.getTopLeftOfTile(row, col)
    pygame.draw.rect(self.surface, TILECOLOR,
       (left, top, self.tilesize, self.tilesize))
    text = self.font.render(label, True, TEXTCOLOR)
    rect = text.get_rect()
    rect.center = left + (self.tilesize / 2), top + (self.tilesize / 2)
    self.surface.blit(text, rect)

  def getTopLeftOfTile(self, row, col):
    left = self.xmargin + col * (self.tilesize + self.gap - 1)
    top = self.ymargin + row * (self.tilesize + self.gap - 1)
    return top, left


def shutdown():
  pygame.quit()
  sys.exit()


def main():
  pygame.init()
  if android:
    android.init()
    android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

  clock = pygame.time.Clock()
  mainsurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
  pygame.display.set_caption('Letter Roller')

  board = Board(5, 5)
  if android:
    boardui = PyGameBoardUI(mainsurface, board, 1)
  else:
    boardui = TermBoardUI(board)

  boardui = PyGameBoardUI(mainsurface, board, 1)

  while True:
    boardui.draw()
    if android and android.check_pause():
      android.wait_for_resume()

    # TODO pause for events rather than busywaiting
    for event in pygame.event.get():
      if event.type == QUIT:
         shutdown()
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
         shutdown()

    pygame.display.update()
    clock.tick(FPS)


if __name__ == '__main__':
  main()
