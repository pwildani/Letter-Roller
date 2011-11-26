"""
Generate a board and print it out.
"""

import board
import sys

class TermBoardUI:
   def __init__(self, board):
     self.board = board

   def draw(self, out=sys.stdout):
     for r in range(self.board.rows):
       print >>out
       for c in range(self.board.cols):
         print >>out, self.board.letterAt(r, c),
     print >>out

def main():
  rows = cols = 5
  if len(sys.argv) > 1:
    rows = cols = int(sys.argv[1])
  if len(sys.argv) > 2:
    cols = int(sys.argv[2])

  print 'Rows: %s, Cols: %s' % (rows, cols)

  ui = TermBoardUI(board.Board(rows, cols))
  ui.draw()
 
if __name__ == '__main__':
  main()
