from pydub import AudioSegment
import pygame as pygame
import os

class Talk_player:

    # 生成播放器物件，同時定義base_path、副檔名，並初始化pygame.mixer
    def __init__(self):
        self.base_path = "./talks/"
        self.mp3 = ".mp3"
        self.wav = ".wav"
        pygame.mixer.init()
        self.music = pygame.mixer.music

    def mp3_to_wav(self, id):
        """將下載的mp3轉成wav格式

        Parameters:
            id: str, talk id為音檔下載時的預設名稱，這裡用來取得音檔
        """

        mp3_talk_path = self.base_path + id + self.mp3
        sound = AudioSegment.from_mp3(mp3_talk_path)

        wav_talk_path = self.base_path + id + self.wav
        sound.export(wav_talk_path, format = "wav")
        return wav_talk_path

    def play_talk(self, talk_id):
        """用Talk_player物件的music屬性播放音檔

        Parameters:
            id: str, talk id為音檔下載時的預設名稱，這裡用來取得音檔
        """
        self.music.load(self.mp3_to_wav(talk_id))
        self.music.play()

    def stop_talk(self):
        """停止播放音檔"""
        self.music.stop()

    def remove_audios(self, talk_id):
        mp3_talk_path = self.base_path + talk_id + self.mp3
        wav_talk_path = self.base_path + talk_id + self.wav

        if os.path.exists(mp3_talk_path):
            os.remove(mp3_talk_path)
        else:
            print(mp3_talk_path, " does not exist")

        if os.path.exists(wav_talk_path):
            os.remove(wav_talk_path)
        else:
            print(wav_talk_path, "does not exist")