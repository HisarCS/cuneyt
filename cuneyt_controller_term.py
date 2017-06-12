from cuneyt import cuneyt
import time


c = cuneyt(motor_setup=1,motor_driver=0)
V = 0
W = 0
while True:
  try:
    key = raw_input()
  except Exception as e:
    key = input()
  
  if key == 'exit':
    c.motors.move(0,0)
    break
  if key == 'q':
    V = 0
    W = 0
  if key == 'o':
    V = 0
  elif key == 'p':
    W = 0
  for k in key:
    if k == 'i':
      V += 0.1
    elif k == 'k':
      V -= 0.1
    elif k == 'j':
      W += 0.4
    elif k == 'l':
      W -= 0.4
  c.motors.move(V,W-.25)
