import pygame
from pygame import mixer

class SoundManager:

    def __init__(self):
        mixer.init()
        mixer.music.load('sfx/atari_st_beat.mp3')
        self.paddle_hit_sound = pygame.mixer.Sound('sfx/paddle_hit.wav')
        self.brick_hit_sound = pygame.mixer.Sound('sfx/brick_hit.wav')
        self.new_row_sound = pygame.mixer.Sound('sfx/punch.wav')
        self.playing_music = False
        self.extravaganza = False

    def start_music(self):
        mixer.music.set_volume(0.05)
        mixer.music.play(-1, 0.0)
        self.playing_music = True

    def stop_music(self):
        mixer.music.stop()
        self.playing_music = False

    def play_paddle_hit_sound(self):
        self.paddle_hit_sound.play()

    def play_brick_hit_sound(self):
        self.brick_hit_sound.play()

    def play_new_row_sound(self):
        self.new_row_sound.play()

    def start_extravaganza(self):
        mixer.music.load('sfx/extravaganza.wav')
        mixer.music.set_volume(0.05)
        mixer.music.play(-1, 0.0)
        self.playing_music = True
        self.extravaganza = True

    def stop_extravaganza(self):
        mixer.music.load('sfx/atari_st_beat.mp3')
        mixer.music.set_volume(0.05)
        mixer.music.play(-1, 0.0)
        self.playing_music = True
        self.extravaganza = False
