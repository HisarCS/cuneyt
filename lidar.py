class lidar:
    def __init__(self,GPIO,time):

        self.GPIO = GPIO
        self.time = time
        self.settle_duration = 1

        #define gpio pins
        #TODO: fix these
        self.u1e = 0
        self.u1t = 0
        self.u2e = 0
        self.u2t = 0
        self.servo = 12
        
        #setup gpio pins
        self.GPIO.setup(u1e,self.GPIO.IN)
        self.GPIO.setup(u1t,self.GPIO.OUT)
        self.GPIO.setup(u2e,self.GPIO.IN)
        self.GPIO.setup(u2t,self.GPIO.OUT)
        
        #set triggers to low
        self.GPIO.output(u1t,False)
        self.GPIO.output(u2t,False)

        #last s1 distance, time s2 distance, time
        self.last_read = [0,0,0,0]
    def read(self):
        #TODO: read sensors simultaneously
        self.GPIO.output(u1t,True)
        time.sleep(0.00001)
        self.GPIO.output(u1t,False)
        while GPIO.input(u1e) == 0:
            pulse_start = time.time()
        while GPIO.input(u1e) == 1:
            pulse_end = time.time()
            if (pulse_end - pulse_start) > 1:
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
                if (pulse_end - pulse_start) > 1:
                    break
        pulse_duration = pulse_end - pulse_start
        self.last_read[2] = pulse_duration * 17150
        self.last_read[3] = pulse_start
        GPIO.output(u1t,False)
        GPIO.output(u2t,False)
