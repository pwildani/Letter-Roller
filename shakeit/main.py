import pygame
import itertools
import time
import math
from collections import namedtuple

try:
    import android
except ImportError:
    class android:
       @staticmethod
       def init(): pass
       @staticmethod
       def accelerometer_enable(_): pass
       @staticmethod
       def accelerometer_reading(): return 1, 2, 3


Sample = namedtuple('Sample', 'ts x y z')
Sample.r = property(lambda s: math.sqrt(s.x * s.x + s.y * s.y + s.z * s.z))

class ShakeSensor:
  SHAKE_EVENT = pygame.USEREVENT

  normalization_threshold_ratio = 0.1

  threshold_distance = 5
  threshold_time = 1.0
  running_seconds = 5

  def __init__(self):
    android.accelerometer_enable(True)
    x, y, z = android.accelerometer_reading()
    self._samples = []
    self._init_time = time.time()
    
    self._normal = None

  def update(self):
    # Take a new sample.
    x, y, z = android.accelerometer_reading()
    ts = time.time()
    self._samples.append(Sample(ts, x, y, z))
    while self._samples and ts - self._samples[0].ts > self.running_seconds:
      del self._samples[0]

    # If it's been long enough since sensor initialization, take a normal
    # reading as a first guess.
    if not self._normal and 1 > time.time() - self._init_time:
      self._normal = Sample(time.time(), x, y, z)

    
    # Shake detection.
    d = Sample(0, 0, 0, 0)
    ad = Sample(0, 0, 0, 0)
    n = self._normal
    prevts = ts
    rsamples = []
    for s in reversed(self._samples):
      rsamples.append(s.r)

      a = Sample(0, s.x - n.x,
                    s.y - n.y,
                    s.z - n.z)
      dt = prevts - s.ts
      dist = Sample(0, dt * a.x, dt * a.y, dt * a.z)
      prevts = s.ts

      d = Sample(d.ts + dt, d.x + dist.x, d.y + dist.y, d.z + dist.z)
      ad = Sample(ad.ts + dt,
          ad.x + abs(dist.x),
          ad.y + abs(dist.y),
          ad.y + abs(dist.z))
      if ad.ts > self.threshold_time:
        if ad.r > self.threshold_distance:
          self.postShakeEvent(d, ad)
        break

    print "new:", s, "r:", s.r, " overall:", d, "r:", d.r, " absolute:", ad, "r:", ad.r, " normal: ", self._normal, "r:", self._normal.r
   
    # Update the gravity vector.
    if rsamples:
      rnorm = reduce(lambda x, y: x*y, rsamples) ** (1.0/len(rsamples))
      if rnorm != 0:
	snorm = Sample(0, 0, 0, 0)
	sn = 0
	for s in self._samples:
	  if abs(1 - s.r / rnorm) < self.normalization_threshold_ratio:
	    sn += 1
	    snorm = Sample(0, snorm.x + s.x, snorm.y + s.y, snorm.z + s.z)
	if sn > 0:
	  snorm = Sample(0, snorm.x / sn, snorm.y / sn, snorm.z / sn)
	  self._normal = snorm

  def postShakeEvent(self, overall, absolute):
    ev = pygame.event.Event(self.SHAKE_EVENT, overall=overall, absolute=absolute)
    print "Shake: ", ev
    pygame.event.post(ev)
    
def main():
  pygame.init()
  if android:
    android.init()
    # android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
    android.accelerometer_enable(True)
  shaker = ShakeSensor()

  clock = pygame.time.Clock()

  main = pygame.display.set_mode((800, 400))
  pygame.display.set_caption('Shake Test')
  FONTFILE = 'freesansbold.ttf'
  font = pygame.font.Font(FONTFILE, 12)

  lastshake = time.time()

  label = 'no shake'
  while True:
    if android:
      shaker.update()
    for ev in pygame.event.get():
      if ev.type == pygame.QUIT:
	sys.exit()
      if ev.type == pygame.KEYDOWN:
	if android and ev.key == android.KEYCODE_BACK:
	  sys.exit()
      if ev.type == ShakeSensor.SHAKE_EVENT:
        label = '%s: %2.4fm, offset: %2.4fm' % (time.time(), ev.absolute.r, ev.overall.r)
        lastshake = time.time()

    color = 255 - (time.time() - lastshake) * 255
    if color > 255: color = 255
    if color < 0: color = 0
    main.fill((color, 0, 0))
    text = font.render(label, True, (255,255, 255))
    main.blit(text, text.get_rect())
    pygame.display.flip()

    clock.tick(15)

if __name__ == '__main__':
  main()
