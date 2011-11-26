import pygame

# TODO adapt to the device
WINDOWWIDTH = 480
WINDOWHEIGHT = 800

# Will attempt no more than this FPS.
MAX_FPS = 15

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHTCYAN = (0, 100, 255)
BLUE = (0, 153, 153)
GREEN = (0, 204, 0)
RED = (255, 0, 0)

class Theme:
  ROUNDING = 8

  @property
  def xmargin(self):
    return self.GAP + self.BORDERSIZE + self.GAP

  @property
  def ymargin(self):
    return self.GAP + self.BORDERSIZE + self.GAP

  def getTopLeftOfTile(self, tilesize, row, col):
    left = self.xmargin + col * tilesize 
    top = self.ymargin + row * tilesize
    return top, left

  def fitTiles(self, num, pixels):
    return (pixels - self.GAP * (num + 1) - self.BORDERSIZE * 2) / num

  def drawEmptyCell(self, surface, top, left, tilesize):
    self.roundrect(surface, self.TILECOLOR,
       (left, top, tilesize, tilesize),
       0, self.ROUNDING, self.ROUNDING )
    self.roundrect(surface, self.TILEBORDERCOLOR,
       (left, top, tilesize, tilesize),
       1, self.ROUNDING, self.ROUNDING)

  def drawCell(self, surface, font, tilesize, row, col, label):
    outersize = tilesize + self.GAP
    top, left = self.getTopLeftOfTile(outersize, row, col)
    self.drawEmptyCell(surface, top, left, tilesize)
    text = font.render(label, True, self.TEXTCOLOR)
    rect = text.get_rect()
    rect.center = left + (outersize / 2), top + (outersize / 2)
    surface.blit(text, rect)

  def roundrect(self, surface, color, rect, width, xr, yr):
    clip = surface.get_clip()
    if not isinstance(rect, pygame.Rect):
      rect = pygame.Rect(rect)
    xr = min(xr, rect.width / 2)
    yr = min(yr, rect.height / 2)

    # Uses clipping and rect/ellipse instead of line and arc so that we can
    # draw solid shapes with the same logic.
    
    # Draw the center cross.
    surface.set_clip(clip.clip(rect.inflate(0, -yr * 2)))
    pygame.draw.rect(surface, color, rect.inflate(1 - width,0), width)
    # TODO fix the wasted overdraw.
    surface.set_clip(clip.clip(rect.inflate(-xr * 2, 0)))
    pygame.draw.rect(surface, color, rect.inflate(0,1 - width), width)

    # Top left corner.
    surface.set_clip(clip.clip(rect.left, rect.top, xr, yr))
    pygame.draw.ellipse(surface, color, pygame.Rect(rect.left, rect.top, 2 * xr, 2 * yr), width)

    # Bottom right corner.
    surface.set_clip(clip.clip(rect.right - xr, rect.bottom - yr, xr, yr))
    pygame.draw.ellipse(surface, color, pygame.Rect(rect.right - 2 * xr, rect.bottom - 2 * yr, 2 * xr, 2 * yr), width)

    # Top right corner.
    surface.set_clip(clip.clip(rect.right - xr, rect.top, xr, yr))
    pygame.draw.ellipse(surface, color, pygame.Rect(rect.right - 2 * xr, rect.top, 2 * xr, 2 * yr), width)

    # Bottom left corner.
    surface.set_clip(clip.clip(rect.left, rect.bottom - yr, xr, yr))
    pygame.draw.ellipse(surface, color, pygame.Rect(rect.left, rect.bottom - 2 * yr, 2 * xr, 2 * yr), width)

    surface.set_clip(clip)

  def tilePixels(self, num, tilesize):
   return num * (tilesize + self.GAP) + self.GAP + self.BORDERSIZE

  def drawBorder(self, surface, rows, cols, tilesize):
    if self.BORDERSIZE:
      width = self.tilePixels(cols, tilesize)
      height = self.tilePixels(rows, tilesize)
      pygame.draw.rect(surface, self.BORDERCOLOR,  (
	  self.BORDERSIZE, self.BORDERSIZE - self.GAP,
	  width, height),
	self.BORDERSIZE)

class GarishTheme(Theme):
  GAP = 1
  BORDERSIZE = 3

  BGCOLOR = BLUE
  TILECOLOR = GREEN
  TILEBORDERCOLOR = RED
  TEXTCOLOR = WHITE
  BORDERCOLOR = LIGHTCYAN

  BUTTONCOLOR = WHITE
  BUTTONTEXTCOLOR = BLACK
  MESSAGECOLOR = WHITE
  FONTFILE = 'freesansbold.ttf'
  FONTRATIO = 2.0 / 3


class PyGameBoardUI:
  def __init__(self, surface, board, theme):
    self.surface = surface
    self.board = board
    self.rows = board.rows
    self.cols = board.cols
    self.theme = theme

    rect = surface.get_rect()
    self.width = rect.width
    self.height = rect.height

    self.bordersize = 3

    self.tilesize = min(theme.fitTiles(self.rows, self.height),
                        theme.fitTiles(self.cols, self.width))

    self.fontsize = int(self.tilesize * theme.FONTRATIO)
    self.font = pygame.font.Font(theme.FONTFILE, self.fontsize)


  def draw(self, theme=None):
    theme = theme or self.theme
    self.surface.fill(theme.BGCOLOR)

    # Render the letters
    for r in range(self.rows):
      for c in range(self.cols):
        theme.drawCell(self.surface, self.font, self.tilesize, r, c, self.board.letterAt(r, c))

    # Render a box around the letters
    theme.drawBorder(self.surface, self.rows, self.cols, self.tilesize)
