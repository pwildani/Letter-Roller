"""
Game state.
"""

import string
import sys
import random

class Board:
  allcubes = ['TTIEII','HORLND','IICELT','NOOWTU', 'MEEAEE','OOOTTU','GROWVR','GEANNM','NUSESS','AEAEEE','GUEEAM','CCNEST','ASIRFY','RASAAF','RRRYIP','DONDHT','PYRFIS','HOLRND','DNANEN','ASARIF','PIECTL','CEIPST','TTTOEM','QXKJZB','ROHDLH']
  # FUTURE TODO: Create cubes algorithmically
  def select_cubes(self,cubes):
    n = self.rows * self.cols
    if n > len(cubes):
      print "Boards of size "+str(self.rows)+"x"+str(self.cols)+" are not yet supported."
      sys.exit()
    return random.sample(cubes,n)

  def shakeit(self):
    '''Shake the cubes and return a 2-D array of faces'''
    letters = []
    for cube in self.cubes:
      letters.extend(random.sample(cube,1))
    self.letters = letters
    return letters
  
  def __init__(self, rows, cols):
    self.rows = rows
    self.cols = cols
    self.cubes = self.select_cubes(self.allcubes) # 1-D list
    self.shakeit()


  def letterAt(self, row, col):
    i = row * self.cols + col
    return self.letters[i]

