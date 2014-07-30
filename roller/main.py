import pygame
import itertools
import pygameui
import events
import board
import shakesensor
import time

try:
    import android
except ImportError:
    android = None

events.KEYDOWN.handler(pygame.K_ESCAPE)(events.handleQuit)



SHAKE_DETECTION_FPS = 100
IDLE_FPS = 4

def main():
  last_touch = [time.time()]
  fps = IDLE_FPS
  if android: fps = SHAKE_DETECTION_FPS

  pygame.init()
  shaker = None
  sensitiveshaker = None
  
  if android:
    android.init()
    android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
    shaker = shakesensor.ShakeSensor()
    sensitiveshaker = shakesensor.ShakeSensor()
    sensitiveshaker.threshold_distance = .5
    sensitiveshaker.threshold_time = 0.5

  @events.KEYDOWN.handler(pygame.K_SPACE)
  @events.EVENTS.handler(shakesensor.ShakeSensor.SHAKE_EVENT)
  def handleShake(game, ev):
    if ev.type == shakesensor.ShakeSensor.SHAKE_EVENT:
      if ev.source is sensitiveshaker and sensitiveshaker.settled:
        fps = SHAKE_DETECTION_FPS
        last_touch[0] = time.time()
        print "FAST!:", ev
        return

    game.shakeit()

  clock = pygame.time.Clock()
  main = pygame.display.set_mode(
      (pygameui.WINDOWWIDTH, pygameui.WINDOWHEIGHT))
  pygame.display.set_caption('Letter Roller')

  game = board.Board(5, 5)
  theme = pygameui.GreyTheme()
  boardui = pygameui.PyGameBoardUI(main, game, theme)
  print "Game init:", game, theme, boardui

  while True:

    if shaker: shaker.update()
    if sensitiveshaker: sensitiveshaker.update()

    boardui.draw()
    pygame.display.flip()
    
    print 'Loop! fps:', clock.get_fps()


    if android and android.check_pause():
      android.wait_for_resume()
      shaker = shakesensor.ShakeSensor()

    for event in pygame.event.get():
      print event
      events.EVENTS[event.type](game, event)

    if (sensitiveshaker and fps != IDLE_FPS and
        time.time() - last_touch[0] > sensitiveshaker.threshold_time):
      fps = IDLE_FPS
      print "SLOW!"

    clock.tick(fps)


if __name__ == '__main__':
  main()
