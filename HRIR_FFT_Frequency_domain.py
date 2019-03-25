from scipy.io import loadmat
import numpy as np
import wave
from scipy.io import wavfile
from scipy import signal

def load_CIPIC_HRIP(left_or_right):
    np.set_printoptions(threshold=1e6)
    # np.set_printoptions(suppress=True,precision=4)

    m = loadmat("hrir_final.mat")
    hrir_l = m["hrir_l"]
    hrir_r = m["hrir_r"]

    if left_or_right == "left":
        out = np.vstack((np.squeeze(hrir_l[:, 8]), np.flip(np.squeeze(hrir_l[:, 40]), 0)))
    elif left_or_right =="right":
        out = np.vstack((np.squeeze(hrir_r[:, 8]), np.flip(np.squeeze(hrir_r[:, 40]), 0)))
    return out


def audio_with_brir(brir):

    # read audio file
    wavepath= "nokia.wav"
    fs, audioIn = wavfile.read(wavepath)
    audioIn = np.array(audioIn)
    audioIn = audioIn / 32767

    # get the length of audio file
    duration = len(audioIn)

    # points_number
    # brir= np.array(brir)
    points_number = brir.shape[1]//2   #之输出列数

    #the number of padding zeros
    remainder = duration % points_number

    if remainder>0:
        padding_zero = points_number-remainder

        audioIn = np.hstack((audioIn , np.zeros(padding_zero)))

    # calcualte the new audio length and a step length for each segment
    step = len(audioIn)//points_number


    # length for window size
    window_N = 512
    window = np.hanning(window_N)

    # pass filter
    lowpass = signal.firwin(1000,(20000/fs)*2,window='hamming')
    highpass = signal.firwin(1001,(20/fs)*2,window='hamming',pass_zero=False)

    #init segment piece
    segment_L = np.zeros((points_number,step))
    segment_R = np.zeros((points_number,step))

    #convolve in the time domain
    # for i in range(points_number):
    #     L = signal.lfilter(brir[:,i*2],1,audioIn[step*i:step*(i+1)])
    #     R = signal.lfilter(brir[:,i*2+1],1,audioIn[step*i:step*(i+1)])
    #
    #     segment_L[i,:] = L
    #     segment_R[i,:] = R



    ################# overlap and add #####################
    L = step              # 5000
    P = hrir.shape[0]     # 200
    total_length = L+P-1  # 5199

    Yn_L_segment = np.zeros((points_number,total_length))
    Yn_R_segment = np.zeros((points_number,total_length))

    zero_padding_Xn = np.zeros(total_length-L)
    print("zero_padding_Xn:",len(zero_padding_Xn))

    zero_padding_Hn = np.zeros(total_length-P)
    print("zero_padding_Hn:",len(zero_padding_Hn))

    # FFT
    for i in range(points_number):
        # zero padding for xn and hn
        Xn = np.hstack((audioIn[step*i: step*(i+1)],zero_padding_Xn))
        Hn_L = np.hstack((brir[:,i*2],zero_padding_Hn))
        Hn_R = np.hstack((brir[:,i*2+1],zero_padding_Hn))

        # print("============",i,"==============")
        # print("Xn:",len(Xn))
        # print("Hn_L:",len(Hn_L))
        # print("Hn_R",len(Hn_R))



        # Do the fft
        Xk = np.fft.fft(Xn)
        Hk_L = np.fft.fft(Hn_L)
        Hk_R = np.fft.fft(Hn_R)

        # convolution in frequency domain
        Yk_L = np.multiply(Xk,Hk_L)
        Yk_R = np.multiply(Xk,Hk_R)

        # Do ifft , convert to time domain   plus abs()
        Yn_L = np.fft.ifft(Yk_L)
        Yn_R = np.fft.ifft(Yk_R)

        # store Y0n,Y1n,Y2n... to a matrix
        Yn_L_segment[i,:] = Yn_L
        Yn_R_segment[i,:] = Yn_R

    Out_Left = np.zeros(len(audioIn) + P - 1)
    Out_Right = np.zeros(len(audioIn) + P - 1)
    # Overlap and add algorithm

    for i in range(points_number):
        Out_Left[i*L:i*L+L+P-1] = Out_Left[i*L:i*L+L+P-1] +Yn_L_segment[i]
        Out_Right[i*L:i*L+L+P-1] = Out_Right[i*L:i*L+L+P-1]+Yn_R_segment[i]
    #np.savetxt('Out_Left.csv', Out_Left, delimiter=",")

# For the first method
#     out_L = segment_L.reshape(-1)
#     out_R = segment_R.reshape(-1)
#     out = np.vstack((out_L,out_R))
#     out = out.T
    # For fft method
    out = np.vstack((Out_Left,Out_Right))
    out = out.T
    print(out.shape)

    return out

if __name__ =='__main__':

    fs = 44100

    hrir_l = load_CIPIC_HRIP('left')
    hrir_r = load_CIPIC_HRIP('right')

    hrir = np.zeros((200, 100))

    for i in range(50):
        hrir[:, i * 2] = hrir_l[i]
        hrir[:, i * 2 + 1] = hrir_r[i]

    out =audio_with_brir(hrir)

    #np.savetxt('fftOUT.csv',out,delimiter=",")

    wavfile.write('FFTnokia.wav',44100,out)
