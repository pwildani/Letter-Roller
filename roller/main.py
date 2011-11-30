import pygame
import itertools
import pygameui
import events
import board
import shakesensor

try:
    import android
except ImportError:
    android = None

events.KEYDOWN.handler(pygame.K_ESCAPE)(events.handleQuit)

@events.KEYDOWN.handler(pygame.K_SPACE)
@events.EVENTS.handler(shakesensor.ShakeSensor.SHAKE_EVENT)
def handleShake(game, ev):
  game.shakeit()

def main():
  pygame.init()
  shaker = None
  if android:
    android.init()
    android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
    shaker = shakesensor.ShakeSensor()

  clock = pygame.time.Clock()
  mainsurface = pygame.display.set_mode(
      (pygameui.WINDOWWIDTH, pygameui.WINDOWHEIGHT))
  pygame.display.set_caption('Letter Roller')

  game = board.Board(5, 5)
  theme = pygameui.GreyTheme()
  boardui = pygameui.PyGameBoardUI(mainsurface, game, theme)

  while True:
    if shaker: shaker.update()

    if android and android.check_pause():
      android.wait_for_resume()
      shaker = shakesensor.ShakeSensor()

    # TODO pause for events rather than busywaiting
    for event in itertools.chain([pygame.event.wait()], pygame.event.get()):
      events.EVENTS[event.type](game, event)

    boardui.draw()
    pygame.display.update()
    clock.tick(pygameui.MAX_FPS)


if __name__ == '__main__':
  main()
