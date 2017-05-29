import cuneyt as cun
import time
import math
cuneyt = cun.cuneyt()

#forward
cuneyt.motors.move(0, 100, 0)
time.sleep(1)
#right
cuneyt.motors.move(math.pi/2,100,0)
time.sleep(1)
#backward
cuneyt.motors.move(math.pi, 100, 0)
time.sleep(1)
#left
cuneyt.motors.move(1.5 * math.pi, 100, 0)
#right dg forward
cuneyt.motors.move(math.pi/4, 100, 0)
time.sleep(1)
#right dg backward
cuneyt.motors.move(1.25 * math.pi, 100, 0)
time.sleep(1)
#left dg forward
cuneyt.motors.move(math.pi/(-4), 100, 0)
time.sleep(1)
#left dg backward
cuneyt.motors.move(.75 * math.pi, 100, 0)
time.sleep(1)

#cuneyt.motors.move(math.pi * 0.333 - 0.25 * math.pi, 100, 0)
#time.sleep(1)
#stop
cuneyt.motors.stop_all()
time.sleep(1)
cuneyt.close()
