from pylab import *

data = loadtxt('EMG.txt')

EMGb=data[:,-1]

figure()
plot(EMGb)
xlabel('Sample #')
ylabel('ADC')
show()

t = arange(len(EMGb))/1000.

nbits=10
Vcc=3.3

G=1000.

EMGv = (EMGb/(2**nbits-1)-.5)*Vcc/2./G
EMGmv = (EMGv-EMGv.mean())*G

figure()
plot(t, EMGmv)
xlabel('t(ms)')
ylabel('mV')
show()
