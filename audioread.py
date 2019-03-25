from scipy.io import loadmat
import numpy as np
import wave
from scipy.io import wavfile
from scipy import signal



X=np.array([2,3,4,5,6,7,8,9,10,11,12,13,14])
H=np.array([1,2,1])  # M
L=5
M = len(H)

# find the number of zero padding
if len(X) % L !=0:
    zero_padding_number = L-(len(X)%L)

#create a array of zero padding
zero_padding = np.zeros(zero_padding_number)

#connect two array together to form new X[n]
X = np.hstack((X,zero_padding))

# calculate number of rows of array
row = len(X)//L

# reshape array every L values, row*L matrics
X = X.reshape(row,L)

# 错位相加最后M-1个点

print(X[1,-(M-1):])



import numpy as np
Xn = np.array([1,1,1,1,0,0]) # L=4
Hn = np.array([1,2,3,0,0,0]) # P=3          L+P-1=6

Xk = np.fft.fft(Xn)
Hk = np.fft.fft(Hn)
Yk = np.multiply(Xk,Hk)

Yn = np.fft.ifft(Yk)               # yn=6

print(abs(Yn))



















# X =[2,3,4]
# H =[1,2,1]

# Y = signal.lfilter(H,1,X)

# X_omega = np.fft.fft(X)
# H_omega = np.fft.fft(H)
#
# Y_omega = np.multiply(X_omega,H_omega)
# Y = np.fft.ifft(Y_omega)



