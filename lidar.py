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

    ''' reads the distance from both ultrasonic sensors in parallel
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

    ''' reads the distance from both ultrasonic sensors in parallel
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
