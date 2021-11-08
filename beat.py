import cv2
import os
import subprocess
import numpy as np
import time
import librosa
from aubio import source, onset
import pyaudio
import wave
import wavio
import matplotlib.pyplot as plt
from ffpyplayer.player import MediaPlayer

video_path = 'Test5.mp4'
audio_path = 'Test5.wav'


def convert_to_audio(video_path):
    command = "ffmpeg -i " + video_path + " -ac 2 -f wav " + audio_path
    subprocess.call(command, shell=True)
    print("Audio Extracted")

def get_onset_times(audio_path):
    window_size = 1024
    hop_size = window_size // 4

    sample_rate = 0
    src_func = source(audio_path, sample_rate, hop_size)
    sample_rate = src_func.samplerate
    onset_func = onset('default', window_size, hop_size)

    duration = float(src_func.duration) / src_func.samplerate

    onset_times = []
    while True:
        samples, num_frames_read = src_func()
        if onset_func(samples):
            onset_time = onset_func.get_last_s()
            if onset_time < duration:
                onset_times.append(onset_time)
            else:
                break
        if num_frames_read < hop_size:
            break

    return onset_times

def get_beat(audio_path):
    #x, sr = librosa.load(audio_path)
    #onset_frames = librosa.onset.onset_detect(x, sr=sr, wait=1, pre_avg=1, post_avg=1, pre_max=1, post_max=1)
    #onset_times = librosa.frames_to_time(onset_frames)

    onset_times = get_onset_times(audio_path)
    round_times = [round(num, 1) for num in onset_times]
    print(str(round_times))
    return round_times
    Print("Beat Analyzed")

def PlayVideo(video_path, beat_times):
    video  = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    sleep_time = int(np.round((1 / fps) * 1000))
    player  = MediaPlayer(video_path)

    if (video.isOpened()== False):
        print("Error opening video  file")


        # Read until video is completed
    while(video.isOpened()):

        ret, frame = video.read()
        audio_frame, val = player.get_frame()

        if ret == False:
            break

        if cv2.waitKey(sleep_time) & 0xFF == ord('q'):
            break

        #if(int(frame_time) in beat_times):
            #print("Beat")

        cv2.imshow('Frame', frame)
        if val != 'eof' and audio_frame is not None:
            img, t = audio_frame
            round_ft = round(t, 1)
            if(round_ft in beat_times):
                print('frame_time: '+ str(t))

    video.release()
    cv2.destroyAllWindows()

#convert_to_audio(video_path)
beat_times = get_beat(audio_path)
PlayVideo(video_path, beat_times)
