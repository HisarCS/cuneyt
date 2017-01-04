import picamera
class camera_controller:

    def __init__(self, pwm):
        #initialize the raspberry pi camera module
        self.camera = picamera.PiCamera()
        #update this
        self.servo_pin = 0
        #add pwm controller as a field
        self.pwm = pwm
        #set recording to false
        self.recording = false
    
    ''' function look_at:
        sets servo angle to the given angle
        note that for our servo and pwn shield, the scaling -angle -> pwm-
        is theta * 3 + 160
    '''
    def look_at(self,angle):
        pwm.setPWM(self.servo_pin, 0, 160 + 3 * angle)

    ''' function take_picture:
        wrapper for camera.capture, saves image with the given name
    '''
    def take_picture(self, name):
        self.camera.capture('./captures' + name)

    ''' function take_picture_at:
        sets servo angle to the given angle and takes a picture
        wrapper for look_at AND take_picture
    '''
    def take_picture_at(self, angle, name):
        self.look_at(angle)
        self.take_picture(name)

    ''' function start_video_recording:
        wrapper for camera.start_recording()
        starts saving the video with the given name
    '''
    def start_video_recording(self, name):
        self.camera.start_recording('./videos' + name)
        self.recording = True

    ''' function stop_video_recording:
        wrapper for camera.stop_recording()
        stops video recording
    '''
    def stop_video_recording(self):
        if (not self.recording):
            raise Exception("Camera not currently recording video")
        else:
            self.camera.stop_recording()

    def capture_vertical_panorama(self, interval):
        raise Exception("Not Yet Implemented")

    def capture_vertical_panorama_at(self, angles):
        raise Exception("Not Yet Implemented")
