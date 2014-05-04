# -*- coding: utf-8 -*-

"""
BITalino API
Created on Tue Jun 25 13:44:28 2013

@author: Priscila Alves

"""
try:
	import bluetooth #from pybluez library
	from bluetooth import discover_devices
except:
	pass
try:
	import serial
	from serial.tools import list_ports
except:
	pass
import time
import math
import numpy

class BITalino:

	def __init__(self):
		self.socket = None
		self.analogChannels = []
		self.number_bytes = None
		self.macAddress = None
		self.serial = False


	def find(self):

		"""
		Search for bluetooth devices nearby

		Output: tuple with name and mac address of each device found
		"""
		try:
			# nearby_devices = discover_devices(lookup_names=True)
			# nearby_devices = list(port[0] for port in list_ports.comports())
			nearby_devices = list(port[0] for port in list_ports.comports() if 'bitalino' in port[0])
			return nearby_devices
		except:
			return -1
			# try:
				#windows
				# nearby_devices = list(port[0] for port in list_ports.comports())
				#mac
				# nearby_devices = list(port[0] for port in list_ports.comports() if 'bitalino' in port[0])
			# except:
				# return -1

	def open(self,macAddress = None, SamplingRate = 1000):

		"""
		Connect to bluetooth device with the mac address provided.
		Configure the sampling Rate.

		Kwargs:

			macAddress (string): MAC address of the bluetooth device
			SamplingRate(int): Sampling frequency (Hz); values available: 1000, 100, 10 and 1

		Output: True or -1 (error)
		"""

		Setup = True
		while Setup:

			if macAddress != None:
				try:
					if ":" in macAddress and len(macAddress) == 17:
						self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
						self.socket.connect((macAddress, 1))
					else:
						self.socket = serial.Serial(macAddress, 115200)
						self.serial = True
					time.sleep(2)

					# Configure sampling rate
					if SamplingRate == 1000:
						variableToSend = 0x03
					elif SamplingRate == 100:
						variableToSend = 0x02
					elif SamplingRate == 10:
						variableToSend = 0x01
					elif SamplingRate == 1:
						variableToSend = 0x00
					else:
						self.socket.close()
						raise TypeError,  "The Sampling Rate %s cannot be set in BITalino. Choose 1000, 100, 10 or 1."%SamplingRate
						return -1

					variableToSend = int((variableToSend<<6)|0x03)
					self.write(variableToSend)
					Setup = False

				except Exception:
					return -1
			else:
				raise TypeError, "A MAC address or serial port is needed to connect"
				return -1
		else:
			self.macAddress = macAddress
			return True

	def start(self, analogChannels = [0,1,2,3,4,5]):

		"""

		Starts Acquisition in the analog channels set.

		Kwargs:

			analogChannels (array of int): channels to be acquired (from 0 to 5)

		Output: True
		"""

		self.analogChannels = analogChannels
		if len(self.analogChannels) == 0 or len(self.analogChannels) > 6 or sum(i > 5 or i<0 for i in analogChannels) > 0 or len(list(set(self.analogChannels))) != len(self.analogChannels):
			raise TypeError, "Analog channels set not valid"
		if self.socket is None:
			raise TypeError, "An input connection is needed."
		bit = 1
		#setting channels mask
		for i in analogChannels:
			bit = bit | 1<<(2+i)

		#start acquisition
		self.write(bit)
		return True

	def stop(self):

		"""
		Sends state value 0 to stop BITalino acquisition.

		Output: True
		"""

		if self.socket is None:
			raise TypeError, "STOP - An input connection is needed."

		# Send stop mode
		self.write(0)

		return True

	def close(self):

		"""
		Closes bluetooth socket

		Output: True
		"""

		# Check
		if self.socket is None:
			raise TypeError, "CLOSE - An input connection is needed."

		self.socket.close()

		return True

	def write(self, data = 0):

		"""
		Send a command to BITalino

		Output: True

		"""
		if self.socket is None:
			raise TypeError, "WRITE - An input connection is needed."

		# Send Mode
		if self.serial:
			self.socket.write(chr(data))
		else:
			self.socket.send(chr(data))
		# time.sleep(1)
		return True

	def battery(self,value = 0):

		"""
		Set the battery threshold of BITalino
		Works only in idle mode

		Kwargs:

			value (int): threshold value from 0 to 63
				0  -> 3.4V
				63 -> 3.8V

		Output: True
		"""

		if self.socket is None:
			raise TypeError, "An input connection is needed."

		# Send Mode
		if 0 <= value <= 63:
			Mode = value << 2
			self.write(Mode)
		else:
			raise TypeError, "The threshold value must be between 0 and 63"

		return True



	def trigger(self,digitalArray = [0,0,0,0]):

		"""
		Act on digital output channels of BITalino
		Works only during acquisition mode

		Kwargs:

			digitalArray (array): array of size 4 which act on digital outputs according to the value: 0 or 1
				Each position of the array corresponds to a digital output, in ascending order.

				Example:
					digitalArray =[1,0,1,0] -> Digital 0 and 2 will be set to one and Digital 1 and 3 to zero

		Output: True

		"""

		if self.socket is None:
			raise TypeError, "An input connection is needed."
		if len(digitalArray) != 4 or sum(i > 1 or i < 0 for i in digitalArray) > 0:
			raise TypeError, "Digital channels set not valid"
		data = 3
		for i,j in enumerate(digitalArray):
			data = data | j<<(2+i)

		self.write(data)
		return True



	def version(self):

		"""

		Get BITalino version
		Works only in idle mode

		Output: Version (string)

		"""

		if self.socket is None:
			raise TypeError, "An input connection is needed."
		self.write(7)
		version = ' '
		while version[-1] != '\n':
			if self.serial:
				version += self.socket.read(1)
			else:
				version += self.socket.recv(1)
		else:
			return version[:-1]

	def read(self, nSamples = 100):

		"""
		Acquire defined number of samples from BITalino

		Kwargs:
			nSamples (int): number of samples

		Output:
			dataAcquired (array): the data acquired is organized in a matrix; The columns correspond to the sequence number, 4 digital channels and analog channels, as configured previously on the start method;
								Each line correspond to a sample.

								The organization of the array is as follows:
								--  Always included --
								Column 0 - Sequence Number
								Column 1 - Digital 0
								Column 2 - Digital 1
								Column 3 - Digital 2
								Column 4 - Digital 3
								-- Variable with the analog channels set on start method --
								Column 5  - analogChannels[0]
								Column 6  - analogChannels[1]
								Column 7  - analogChannels[2]
								Column 8  - analogChannels[3]
								Column 9  - analogChannels[4]
								Column 10 - analogChannels[5]
		"""

		if self.socket is None:
			raise TypeError, "An input connection is needed."
		nChannels = len(self.analogChannels)

		if nChannels <=4 :
			self.number_bytes = int(math.ceil((12.+10.*nChannels)/8.))
		else:
			self.number_bytes = int(math.ceil((52.+6.*(nChannels-4))/8.))

		#get Data according to the value nSamples set
		dataAcquired = numpy.zeros((5+nChannels,nSamples))
		Data = ''
		sampleIndex = 0
		while sampleIndex < nSamples:
			while len(Data) < self.number_bytes:
				if self.serial:
					Data += self.socket.read(1)
				else:
					Data += self.socket.recv(1)
			else:
				decoded = self.decode(Data)
				if len(decoded) != 0:
					dataAcquired[:,sampleIndex] = decoded.T
					Data = ''
					sampleIndex+=1

				else:
					if self.serial:
						Data += self.socket.read(1)
					else:
						Data += self.socket.recv(1)
					Data = Data[1:]
					print "ERROR DECODING"

		else:
			return dataAcquired


	def decode(self,data,nAnalog = None):

		"""

		Unpack data samples.

		Kwargs:

			data (array): received data
			nAnalog (int): number of analog channels contained in data

		Output:
			res(array): data unpacked
		"""

		if nAnalog == None: nAnalog = len(self.analogChannels)
		if nAnalog <=4 :
			number_bytes = int(math.ceil((12.+10.*nAnalog)/8.))
		else:
			number_bytes = int(math.ceil((52.+6.*(nAnalog-4))/8.))

		nSamples = len(data)/number_bytes
		res = numpy.zeros(((nAnalog+5),nSamples))

		j,x0,x1,x2,x3,out,inp,col,line = 0,0,0,0,0,0,0,0,0
		encode0F = int('\x0F'.encode("hex"),16)
		encode01 = int('\x01'.encode("hex"),16)
		encode03 = int('\x03'.encode("hex"),16)
		encodeFC = int('\xFC'.encode("hex"),16)
		encodeFF = int('\xFF'.encode("hex"),16)
		encodeC0 = int('\xC0'.encode("hex"),16)
		encode3F = int('\x3F'.encode("hex"),16)
		encodeF0 = int('\xF0'.encode("hex"),16)

		#CRC check
		CRC = int(data[j+number_bytes-1].encode("hex"),16) & encode0F
		for byte in range(number_bytes):
			for bit in range(7,-1,-1):
				inp=int(data[byte].encode("hex"),16)>>bit & encode01
				if byte == (number_bytes - 1) and bit<4:
					inp = 0
				out=x3
				x3=x2
				x2=x1
				x1=out^x0
				x0=inp^out

		if CRC == int((x3<<3)|(x2<<2)|(x1<<1)|x0):
			try:

				# Seq Number
				SeqN = int(data[j+number_bytes-1].encode("hex"),16) >> 4 & encode0F
				res[line,col] = SeqN
				line +=1

				# Digital 0
				Digital0 = int(data[j+number_bytes-2].encode("hex"),16) >> 7 & encode01
				res[line,col]=Digital0
				line +=1

				# Digital 1
				Digital1 = int(data[j+number_bytes-2].encode("hex"),16) >> 6 & encode01
				res[line,col] = Digital1
				line +=1

				# Digital 2
				Digital2 = int(data[j+number_bytes-2].encode("hex"),16) >> 5 & encode01
				res[line,col] = Digital2
				line +=1

				# Digital 3
				Digital3 = int(data[j+number_bytes-2].encode("hex"),16) >> 4 & encode01
				res[line,col] = Digital3
				line +=1

				if number_bytes >=3:

					# Analog 0
					Analog0 = (int(data[j+number_bytes-2].encode("hex"),16) & encode0F) << 6 | (int(data[j+number_bytes-3].encode("hex"),16) & encodeFC) >> 2
					res[line,col] = Analog0
					line +=1

				if number_bytes >=4:

					# Analog 1
					Analog1 = (int(data[j+number_bytes-3].encode("hex"),16) & encode03) << 8 | (int(data[j+number_bytes-4].encode("hex"),16) & encodeFF)
					res[line,col] = Analog1
					line +=1

				if number_bytes >=6:

					# Analog 2
					Analog2 = (int(data[j+number_bytes-5].encode("hex"),16) & encodeFF) << 2 | (int(data[j+number_bytes-6].encode("hex"),16) & encodeC0) >> 6
					res[line,col] = Analog2
					line +=1

				if number_bytes >=7:

					# Analog 3
					Analog3 = (int(data[j+number_bytes-6].encode("hex"),16) & encode3F) << 4 | (int(data[j+number_bytes-7].encode("hex"),16) & encodeF0) >> 4
					res[line,col] = Analog3
					line +=1

				if number_bytes >=8:

					# Analog 4
					Analog4 = (int(data[j+number_bytes-7].encode("hex"),16) & encode0F) << 2 | (int(data[j+number_bytes-8].encode("hex"),16) & encodeC0) >> 6
					res[line,col] =Analog4*(1023/63)
					line +=1

					# Analog 5
					if numpy.shape(res)[0] == 11:
						Analog5 = int(data[j+number_bytes-8].encode("hex"),16) & encode3F
						res[line,col] = Analog5*(1023/63)

			except Exception:
				print "exception decode"
			return res
		else:
			return []


if __name__ == '__main__':

	#Example
	device = BITalino()

	macAddress = "00:13:01:04:02:16"
	#macAddress = "/dev/tty.bitalino-DevB"
	SamplingRate = 1000
	nSamples = 10

	# Connect to bluetooth device and set Sampling Rate
	device.open(macAddress, SamplingRate)

	#set battery threshold
	th = device.battery(20)

	#get BITalino version
	BITversion = device.version()
	print "version: ",BITversion

	#Start Acquisition in Analog Channels 0 and 3
	device.start([0,3])

	#Read 1000 samples
	dataAcquired = device.read(nSamples)

	# turn BITalino led on
	device.trigger([0,0,1,0])

	#stop acquisition
	device.stop()
	device.close()


	SeqN = dataAcquired[0,:]
	D0 = dataAcquired[1,:]
	D1 = dataAcquired[2,:]
	D2 = dataAcquired[3,:]
	D3 = dataAcquired[4,:]
	A0 = dataAcquired[5,:]
	A3 = dataAcquired[6,:]
	print SeqN
