import pyglet as audio
import wave
import config

class resources:
    def __init__(self):
	self.path = config.resource_folder
	
    def play_audio_file(self, file):
	music = pyglet.media.load(self.path+'/'+file, streaming=False)
	music.play()
