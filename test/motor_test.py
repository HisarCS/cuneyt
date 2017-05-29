import cuneyt as Cuneyt
import math, time
cuneyt = Cuneyt.cuneyt()
directions = ["forward", "right", "backward", "left"]
turns = ["clockwise", "counter clockwise"]

cuneyt.logger.info("started motor test")
time.sleep(1)

for x in xrange(4):
  cuneyt.logger.info("going" + directions[x])
  cuneyt.motor_controller.translate((math.pi/2 * x), 100)
  time.sleep(5)
  cuneyt.motor_controller.stop()

for x in xrange(2):
  cuneyt.logger.info("turning" + turns[x])
  cuneyt.motor_controller.turn(x * 200 - 100)
  time.sleep(5)

