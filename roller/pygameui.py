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

BGCOLOR = BLUE
TILECOLOR = GREEN
TILEBORDERCOLOR = RED
TEXTCOLOR = WHITE
BORDERCOLOR = LIGHTCYAN

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE


class PyGameBoardUI:
  def __init__(self, surface, board, gap):
    self.surface = surface
    self.board = board
    self.rows = board.rows
    self.cols = board.cols

    rect = surface.get_rect()
    self.width = rect.width
    self.height = rect.height

    self.bordersize = 3
    self.gap = gap
    self.xmargin = gap + self.bordersize + gap
    self.ymargin = gap + self.bordersize + gap


    totaltilewidth = self.width - gap * (self.cols + 1) - self.bordersize * 2
    fitwidth = totaltilewidth / self.cols

    totaltileheight = self.height - gap * (self.rows + 1) - self.bordersize * 2
    fitheight = totaltileheight / self.rows

    self.innertile = min(fitwidth, fitheight)
    self.outertile = self.innertile + gap

    self.fontsize = self.innertile * 2 / 3
    self.font = pygame.font.Font('freesansbold.ttf', self.fontsize)

  def getTopLeftOfTile(self, row, col):
    left = self.xmargin + col * self.outertile
    top = self.ymargin + row * self.outertile
    return top, left

  def draw(self):
    self.surface.fill(BGCOLOR)

    # Render the letters
    for r in range(self.rows):
      for c in range(self.cols):
        self.drawCell(r, c, self.board.letterAt(r, c))

    # Render a box around the letters
    width = self.cols * self.outertile + self.gap + self.bordersize
    height = self.rows * self.outertile + self.gap + self.bordersize
    pygame.draw.rect(self.surface, BORDERCOLOR,  (
        self.bordersize, self.bordersize - self.gap,
        width, height),
      self.bordersize)

  def drawCell(self, row, col, label):
    top, left = self.getTopLeftOfTile(row, col)
    rounding = 8
    self.roundrect(self.surface, TILECOLOR,
       (left, top, self.innertile, self.innertile),
       0, rounding, rounding )
    self.roundrect(self.surface, TILEBORDERCOLOR,
       (left, top, self.innertile, self.innertile),
       1, rounding, rounding)
    
    text = self.font.render(label, True, TEXTCOLOR)
    rect = text.get_rect()
    rect.center = left + (self.outertile / 2), top + (self.outertile / 2)
    self.surface.blit(text, rect)

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
