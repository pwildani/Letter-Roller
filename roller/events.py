import pygame
import sys

NO_ACTION = lambda _state, _event: None

class EventRegistry(dict):

  def __missing__(self, key):
    return NO_ACTION

  def category(self, event_type):
    def subCategory_(distinguisher):
      target = self.makeSubCategoryRegistry(event_type, distinguisher)
      self[event_type] = lambda state, ev: target[distinguisher(state, ev)](state, ev)
      return target
    return subCategory_

  def makeSubCategoryRegistry(self, event_type, distinguisher):
    return self.__class__()

  def handler(self, value):
    def handler_(implementation):
      self[value] = implementation
      return implementation
    return handler_
  
EVENTS = EventRegistry()

@EVENTS.category(pygame.KEYDOWN)
def KEYDOWN(_, ev):
  return ev.key

@EVENTS.category(pygame.KEYUP)
def KEYUP(_, ev):
  return ev.key

@EVENTS.handler(pygame.QUIT)
def handleQuit(_state, _event):
  pygame.quit()
  sys.exit()

