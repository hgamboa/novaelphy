# -*- coding: utf-8 -*-
from BITalino import *
from pylab import *

device = BITalino()

device.open("98:d3:31:b2:12:36", 1000)

print device.version()

device.start(); data=device.read(5000); device.stop()

device.close()

plot(data[8,:])

xlabel('Sample #')
ylabel('ADC')

show()
