import numpy as np


Xn = np.array([2,3,4,5,6,7,8,9,10,11,12,13,14]) # L=13
Hn = np.array([1,2,1]) # P=3          L+P-1=6

L = len(Xn)
P = len(Hn)
points_number = 3
remainder = L % points_number
if remainder>0:
    zero_padding = points_number - remainder
    Xn = np.hstack((Xn,np.zeros(zero_padding)))

step = len(Xn)//points_number  #5

L =step

total_length = L+P-1

zero_padding_Xn = np.zeros(total_length-L)
zero_padding_Hn = np.zeros(total_length-P)

Ynn = np.zeros((points_number,total_length))


# Xn = np.hstack((Xn[step*0:step*(0+1)],zero_padding_Xn))
# Hn = np.hstack((Hn,zero_padding_Hn))
# Xk = np.fft.fft(Xn)
# Hk = np.fft.fft(Hn)
# Yk = np.multiply(Xk,Hk)
# Yn = np.fft.ifft(Yk)



for i in range(points_number):
    Xn_new = np.hstack((Xn[step*i:step*(i+1)],zero_padding_Xn))
    Hn_new = np.hstack((Hn,zero_padding_Hn))
    Xk = np.fft.fft(Xn_new)
    Hk = np.fft.fft(Hn_new)
    Yk = np.multiply(Xk,Hk)
    Yn = abs(np.fft.ifft(Yk))
    Ynn[i,:] = Yn

# for i in range(points_number):
Out = np.zeros(len(Xn)+zero_padding)
Out[0:L+P-1] = Out[0:L+P-1] + Ynn[0]
Out[1*L:1*L+L+P-1] = Out[1*L:1*L+L+P-1] +Ynn[1]
Out[2*L:2*L+L+P-1] = Out[2*L:2*L+L+P-1] +Ynn[2]

print(Out)


