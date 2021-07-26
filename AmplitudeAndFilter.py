from pyo import *
import matplotlib.pyplot as plt
import math as math

#function for Log Amplitude
def amp(dist):
    if dist == 0:
        return 1
    else:
        return 1.63678 * (0.59776 ** dist)

#function for Lin Frequency
def frequency(dist):
    return -550*dist + 20000

#Boot and Start pyo server
s = Server(duplex=1, buffersize=1024, winhost='asio', nchnls=2).boot()
print('Server Booted')

# sound path
snd_path = 'sounds/A Prayer In Spring.wav'

# Takes User input for distance
dist = int(input('Enter a distance: '))
if dist == 0:
    dist = 1

# Fills a list with amplitude multipliers based on input distance
expTableList = []
counter = 0
for i in range(dist, 66):
    expTableList.append((counter, amp(i)))
    counter += 1

# Create LogTable with logTableList
expt = ExpTable(expTableList)

#Use Phasor + TableRead
lPhasor = Phasor(0.00001)
AmpRead = TableRead(expt, lPhasor).play()

#Play Sound with changing Volume
sV = SfPlayer(snd_path, loop=True, mul=AmpRead)

#Fills a list with Filter Frequency based on input distance
linTableList = []
counter2 = 0
for i in range(dist, 18):
    linTableList.append((counter2, frequency(i)))
    counter2 += 1

#Create LinTable with linTableList
lint = LinTable(linTableList)

#Use Phasor + Table Read
freq = TableRead(lint, lPhasor).play()

#Play sound with changing filter
sF = Tone(sV, freq=freq, mul=1).mix(2).out()

#Show Spectrum
Spectrum(sF)

# Visual Plot of LogTable
fig,ax = plt.subplots()
plt.xlim(0, 66)
ax.grid(color='black')
ax.plot(logt.getTable())
# plt.show()

s.gui(locals())
