# -*- coding: utf-8 -*-

import BITalino 

import numpy
import time
import signal

def signal_handler(signal, frame):
    global device
    print "STOP"
    device.stop()
    device.close()

signal.signal(signal.SIGINT, signal_handler)

macAddress= "98:d3:31:b1:83:96"
#macAddress='/dev/tty.bitalino-DevB'

SamplingRate = 1000
nFrames = 100
threshold = 20

device = BITalino.BITalino()
device.open(macAddress, SamplingRate = SamplingRate)
time.sleep(1)

device.start([0])
print "START"

while True:
    try:
        dataAcquired = device.read(nFrames)
            
        EMG = dataAcquired[-1,:]
        
        value = numpy.mean(abs(EMG-numpy.mean(EMG)))
        #print "v = ", value
        
        if value >= threshold:
            device.trigger([1,1,1,1])
            #print 'on'
        else:
            device.trigger([0,0,0,0])
    except:
        break

