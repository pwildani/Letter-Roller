"""
Game state.
"""

import string

class Board:
  def __init__(self, rows, cols):
    self.rows = rows
    self.cols = cols

  def letterAt(self, row, col):
    # TODO real code
    i = row * self.cols + col
    return string.letters[i % len(string.letters)].upper()

