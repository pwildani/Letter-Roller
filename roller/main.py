import pygame
import sys
import string

import pygameui
import events

try:
    import android
except ImportError:
    android = None


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

events.KEYDOWN.handler(pygame.K_ESCAPE)(events.handleQuit)

def main():
  pygame.init()
  if android:
    android.init()
    android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

  clock = pygame.time.Clock()
  mainsurface = pygame.display.set_mode(
      (pygameui.WINDOWWIDTH, pygameui.WINDOWHEIGHT))
  pygame.display.set_caption('Letter Roller')

  board = Board(5, 5)
  boardui = pygameui.PyGameBoardUI(mainsurface, board, 1)

  while True:
    boardui.draw()
    if android and android.check_pause():
      android.wait_for_resume()

    # TODO pause for events rather than busywaiting
    for event in pygame.event.get():
      events.EVENTS[event.type](board, event)

    pygame.display.update()
    clock.tick(pygameui.FPS)


if __name__ == '__main__':
  main()
