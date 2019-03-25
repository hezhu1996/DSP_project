from scipy.io import loadmat
import numpy as np
import wave
from scipy.io import wavfile
from scipy import signal

def load_CIPIC_HRIP(left_or_right):
    np.set_printoptions(threshold=1e6)
    # np.set_printoptions(suppress=True,precision=4)

    m = loadmat("D:\File\\UOttawa\DSP\Project\Matlab_HRTF\HRTF/hrir_final.mat")
    hrir_l = m["hrir_l"]
    hrir_r = m["hrir_r"]

    if left_or_right == "left":
        out = np.vstack((np.squeeze(hrir_l[:, 8]), np.flip(np.squeeze(hrir_l[:, 40]), 0)))
    elif left_or_right =="right":
        out = np.vstack((np.squeeze(hrir_r[:, 8]), np.flip(np.squeeze(hrir_r[:, 40]), 0)))
    return out


def audio_with_brir(brir):

    # read audio file
    wavepath= "D:\File\\UOttawa\DSP\Final_Project\Final_Project\Matlab-master\HRTF\nokia.wav"
    fs, audioIn = wavfile.read(wavepath)
    audioIn = np.array(audioIn)
    audioIn = audioIn / 32767

    # get the length of audio file
    duration = len(audioIn)

    #points_number
    # brir= np.array(brir)
    points_number = brir.shape[1]/2   #之输出列数

    #the number of padding zeros
    remainder = duration%points_number

    if remainder>0:
        padding_zero = points_number-remainder
        audioIn = np.array([audioIn,np.zeros(3)])

    # calcualte the new audio length and a step length for each segment
    step = len(audioIn)/points_number

    # length for window size
    window_N = 512
    window = np.hanning(window_N)

    # pass filter
    lowpass = signal.firwin(1000,(20000/fs)*2,window='hamming')
    highpass = signal.firwin(1000,(20/fs)*2,window='hamming',pass_zero=False)

    #init segment piece
    segment_L = np.zeros((points_number,step))
    segment_R = np.zeros((points_number,step))

    for i in range(points_number):




if __name__ =='__main__':

    fs = 44100


    hrir_l = load_CIPIC_HRIP('left')
    hrir_r = load_CIPIC_HRIP('right')

    hrir = np.zeros((200, 100))

    for i in range(50):
        hrir[:, i * 2] = hrir_l[i]
        hrir[:, i * 2 + 1] = hrir_r[i]

    audio_with_brir()

