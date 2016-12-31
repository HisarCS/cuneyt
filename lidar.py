import time
class lidar:
    def __init__(self, GPIO, pwm):

        #initialize self fields
        self.pwm = pwm
        self.GPIO = GPIO
        self.time = time
        self.settle_duration = 1

        #define GPIO pins
        #TODO: fix these
        self.u1e = 0
        self.u1t = 0
        self.u2e = 0
        self.u2t = 0
        self.servo = 12
        
        #setup GPIO pins
        self.GPIO.setup(u1e,self.GPIO.IN)
        self.GPIO.setup(u1t,self.GPIO.OUT)
        self.GPIO.setup(u2e,self.GPIO.IN)
        self.GPIO.setup(u2t,self.GPIO.OUT)
        
        #set triggers to low
        self.GPIO.output(u1t,False)
        self.GPIO.output(u2t,False)

        #set servo position to 0
        #TODO: actually do this
        self.servo_position = 0
        self.servo_increment = 2

        #last s1 distance, time s2 distance, time
        self.last_read = [0,0,0,0]
        #environment array
        self.environment = [None] * 180


    ''' function read_sequential
        reads the distance from both ultrasonic sensors in parallel
        saves the values(in meters) to self.last_read, in order defined above
        code automatically breaks if time passed exceeds 100ms,
        note that in 10ms, note that in 10ms, the signal should've travelled
        1.6 meters far and back, we ignore sensor readings larger than 1.6meters and
        return -171.6
    '''

    def read_sequential(self):
        self.GPIO.output(u1t,True)
        time.sleep(0.00001)
        self.GPIO.output(u1t,False)
        while GPIO.input(u1e) == 0:
            pulse_start = time.time()
        while GPIO.input(u1e) == 1:
            pulse_end = time.time()
            if (pulse_end - pulse_start) > 0.01:
                pulse_end = pulse_start-1
                break
        pulse_duration = pulse_end - pulse_start
        self.last_read[0] = pulse_duration * 17150
        self.last_read[1] = pulse_start

        self.GPIO.output(u2t,True)
        time.sleep(0.00001)
        self.GPIO.output(u2t,False)
        while GPIO.input(u2e) == 0:
            pulse_start = time.time()
            while GPIO.input(u2e) == 1:
                pulse_end = time.time()
                if (pulse_end - pulse_start) > 0.01:
                    pulse_end = pulse_Start-1
                    break
        pulse_duration = pulse_end - pulse_start
        self.last_read[2] = pulse_duration * 171.6
        self.last_read[3] = pulse_start
        GPIO.output(u1t,False)
        GPIO.output(u2t,False)
        return self.last_read

    ''' function read_parallel
        reads the distance from both ultrasonic sensors in parallel
        saves the values(in meters) to self.last_read, in order defined above
        code automatically breaks if time passed exceeds 100ms,
        note that in 10ms, note that in 10ms, the signal should've travelled
        1.6 meters far and back, we ignore sensor readings larger than 1.6meters and
        return -171.6
    '''
    def read_parallel(self):
        self.GPIO.output(u1t,True)
        self.GPIO.output(u2t,True)
        time.sleep(0.00001)
        self.GPIO.output(u1t,False)
        self.GPIO.output(u2t,False)
        sens1, sens2 = False, False
        pulse_start1, pulse_start2 = 0, 0
        while True:
            if a and b:
                break
            
            #breaks if time passed exceeds 100ms
            elif (((time.time() - pulse_start1) > 0.01) or
                 ((time.time() - pulse_start2) > 0.01)):
                pulse_end1 = pulse_start1-1
                pulse_end2 = pulse_start2-1
                break

            if GPIO.input(u1e) == 0:
                pulse_start1 = time.time()
                a = True
            if GPIO.input(u2e) == 0:
                pulse_start2 = time.time()
                b = True
        pulse_end1, pulse_end2 = pulse_start1, pulse_start2
        a,b = False,False
        while True:
            if a and b:
                break
            if GPIO.input(u1e) == 1:
                pulse_end1 = time.time()
                a = True
            if GPIO.input(u2e) == 1:
                pulse_end2 = time.time()
                b = True
        self.last_read[0] = (pulse_end1 - pulse_start1) * 171.6
        self.last_read[1] = pulse_start1
        self.last_read[2] = (pulse_end2 - pulse_start2) * 171.6
        self.last_read[3] = pulse_start2
        GPIO.output(u1t,False)
        GPIO.output(u2t,False)
        return self.last_read

    ''' function sweep
        constantly scanse the environment and records the distances from cuneyt
        in all directions, updates the self.environment array with tuples 
        (angle,distance,last_read) runs indefinitely
    '''
    def sweep(self):
        while True:
            if self.servo_position == 0:
                self.servo_increment = 2
            elif self.servo_position == 180:
                self.servo_increment = -2
            self.servo_position = self.servo_position + self.servo_increment
            #TODO: write self.servo_position to the actual servo
            sensors = self.read_parallel()
            self.environment[servo_position / 2] = (self.servo_position,
                                                    sensors[0],
                                                    sensors[1])
            self.environment[servo_position / 2 + 90] = (self.servo_position+90,
                                                         sensors[2],
                                                         sensors[3])
            self.time.sleep(0.5)   

