from cuneyt import cuneyt
import time


c = cuneyt(motor_setup=1,motor_driver=0)
V = 0
W = 0
while True:

  key = raw_input()
  if key == 'q':
    V = 0
    W = 0
  for k in key:
    if k == 'i':
      V += 0.1
    elif k == 'k':
      V -= 0.1
    elif k == 'l':
      W += 0.1
    elif k == 'j':
      W -= 0.1
  c.motors.move(V,W)
