from pygame import mixer

class SoundManager:

    def __init__(self):
        # Initialise mixer
        mixer.init()

        # Load music
        mixer.music.load('sfx/atari_st_beat.mp3')

        # Load sound effects
        self.paddle_hit_sound = mixer.Sound('sfx/paddle_hit.wav')
        self.brick_hit_sound = mixer.Sound('sfx/brick_hit.wav')
        self.new_row_sound = mixer.Sound('sfx/punch.wav')
        self.wall_hit_sound = mixer.Sound('sfx/wall_hit.wav')

        self.playing_music = False   # Indicates if music is currently playing
        self.extravaganza = False   # Indicates if extravaganza music is currently playing

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
    
    def play_wall_hit_sound(self):
        self.wall_hit_sound.play()

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
