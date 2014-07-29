"""
Game state.
"""

import string
import sys
import random
from collections import namedtuple

#WORDLIST = '/usr/share/dict/words'
WORDLIST = 'wordsEn.txt' #SIL Wordlist; less stupid

def get_wordlist():
  fo = open(WORDLIST,'r')
  words = []
  for line in fo:
    if line[0].islower(): # Hack to ditch proper nouns
      words.append(line.strip().upper())
  return sorted(words)

class Board:
  fivecubes = ['TTIEII','HORLND','IICELT','NOOWTU', 'MEEAEE','OOOTTU','GROWVR','GEANNM','NUSESS','AEAEEE','GUEEAM','CCNEST','ASIRFY','RASAAF','RRRYIP','DONDHT','PYRFIS','HOLRND','DNANEN','ASARIF','PIECTL','CEIPST','TTTOEM','QXKJZB','ROHDLH']
  
  def __init__(self, rows, cols):
    self.rows = rows
    self.cols = cols
    self.cubes = self.select_cubes(self.fivecubes) # 1-D list
    self.letters = self.shakeit()

  def select_cubes(self,cubes):
    n = self.rows * self.cols
    if n > len(cubes):
      print "Boards of size "+str(self.rows)+"x"+str(self.cols)+" are not yet supported."
      sys.exit()
    return random.sample(cubes,n)

  def shakeit(self):
    '''Shake the cubes and return a 1-D array of letters'''
    letters = []
    random.shuffle(self.cubes)
    for cube in self.cubes:
      letters.extend(random.sample(cube,1))
    return letters
  
  def grid_letters(self):
    gridded_letters=[]
    r = 0
    c = 0
    for letter in self.letters:
      gridded_letters.append((letter,r,c))
      r += 1
      if r == self.rows:
        r = 0
        c += 1
    return gridded_letters
  
  def word_search(self,word_list, min_size=4):
    gridded_letters = self.grid_letters()
    '''Return all words that are longer than min_size'''
    words = []
    for letter in gridded_letters:
      start_point = letter
      words.extend(word_dfs(start_point,gridded_letters,word_list,self.rows,self.cols))
    return [w for w in words if len(w)>=min_size]

  def letterAt(self, row, col):
    i = row * self.cols + col
    return self.letters[i]

  def print_board(self):
    gridded_letters = self.grid_letters()
    gridded_letters = sorted(gridded_letters,key=lambda x:x[1])
    r=0
    print '___________'
    for i in gridded_letters:
      if i[1]!=r:
        r +=1
        print
      print i[0],
    print
    print '___________'
    return True

    
######

def is_word_prefix(mystr, wordlist):
  return any(x.startswith(mystr) for x in wordlist)

def is_word(mystr,wordlist):
  return mystr in wordlist

def prune_wordlist(letters,wordlist,abbrev=False):
  # ditch any word that contains a letter we don't have
  letter_set = set(letters)
  reduced_wordlist=set([])
  for word in wordlist:
    if all(i in letter_set for i in word):
      reduced_wordlist.add(word)
  if not abbrev:
    s=set([])
    vowels=['A','E','I','O','U','Y']
    for word in reduced_wordlist:
      if any(i in vowels for i in word):
        s.add(word)
    reduced_wordlist = s
  return list(reduced_wordlist)


def word_dfs(start_node,gridded_letters,word_list,rows,cols):
  '''s a w
     e o f 
     j s d '''
  words=[]
  node = namedtuple('node','visited')
  def word(path):
    return ''.join([x[0] for x in path])

  def neighbors(path):
    r = path[-1][1]
    c = path[-1][2]
    for i in (-1, 0, 1):
      if not 0 <= r + i < rows: continue
      for j in (-1, 0, 1):
        if not 0 <= c + j < cols: continue
        index  = (r+i) + rows * (c+j)
        letter = gridded_letters[index]
        #print letter, (r, c, i, j), "->", index
        if letter not in path:
          yield letter

  stack = [[start_node]]
  while stack:
    current = stack.pop()
    cword = word(current)
    if not is_word_prefix(cword, word_list):
      continue # Cannot be a word.
    if is_word(cword, word_list):
      words.append(cword)
      word_list.remove(cword)
    for letter in neighbors(current):
      if is_word_prefix(word(current+[letter]),word_list):
        stack.append(current + [letter])
  return words



def test_word_search(board):
  #wordlist = ['SAW','WAOD','WA','FEJ','SEZ']
  #wordlist.sort()
  wordlist = prune_wordlist(board.letters,get_wordlist())
  print "Pruning complete"
  print board.word_search(wordlist,3)


def test(n):
  b = Board(n, n)
  b.print_board()
  return test_word_search(b)

if __name__ == '__main__':
  import sys
  n=3
  if len(sys.argv)>1:
    n = int(sys.argv[1])
  test(n)
