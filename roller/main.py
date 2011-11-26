import pygame

import pygameui
import events

try:
    import android
except ImportError:
    android = None

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

  game = board.Board(5, 5)
  boardui = pygameui.PyGameBoardUI(mainsurface, game, 1)

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
