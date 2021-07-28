from pyo import *
import matplotlib.pyplot as plt
import math as math

#function for Log Amplitude
def amp(dist):
    if dist == 0:
        return 1
    else:
        return 1.63678 * (0.59776 ** dist)

#Boot and Start pyo server
s = Server(duplex=1, buffersize=1024, winhost='asio', nchnls=2).boot()
print('Server Booted')

# record
path = os.path.join(os.path.expanduser("~"), "Desktop", "test4.wav")
# Record for 10 seconds a 24-bit wav file.
i = Input(0).out()
s.recordOptions(dur=10, filename=path, fileformat=0, sampletype=1)
s.recstart()

# sound path
mainSnd_path = 'sounds/comptinedunautreete_badquality.wav'
AmbiSnd_path = 'sounds/ocean_binaural2stereo.wav'

# Takes User input for distance
dist = int(input('Enter a distance: '))

# Fills a list with amplitude multipliers based on input distance
expTableList = []
counter = 0
for i in range(dist, 66):
    expTableList.append((counter, amp(i)))
    counter += 1

# Create LogTable with logTableList
expt = ExpTable(expTableList)

#Use Phasor + TableRead
Phasor = Phasor(0.000001)
AmpRead = TableRead(expt, Phasor).play()

#Play Sound with changing Volume
sV = SfPlayer(mainSnd_path, loop=True, mul=AmpRead)

#Create LinTable with linTableList
lint = LinTable([(0, 15000), (5, 500), (100, 500)]) # CAN/SHOULD BE CHANGED

#Use Phasor + Table Read
freq = TableRead(lint, Phasor).play()

#Play sound with changing filter
sF = Tone(sV, freq=freq, mul=1)

# Binaural Rendering
ele = 30
azi = Sine(0.1).range(0,360)
binaural_renderer = Binaural(sF, azimuth=azi, elevation=ele, azispan=0, elespan=0)
binaural_renderer.ctrl(title='Binaural Renderer')

# Cross Synthesis with Ambient Background Noise
pva1 = PVAnal(binaural_renderer)
Amb = SfPlayer(AmbiSnd_path, loop=True, mul=1)
pva2 = PVAnal(Amb)

fadet = LogTable([(0, 0.25), (35, 1), (100, 1)]) # CAN/SHOULD BE CHANGED
fade = TableRead(fadet, Phasor).play()
pvc = PVCross(pva1, pva2, fade=fade)
pvc.ctrl(title='Cross')
pvs = PVSynth(pvc).out()

#Show Spectrum
Spectrum(pvs)

# Visual Plot of LogTable
fig,ax = plt.subplots()
plt.xlim(0, 66)
ax.grid(color='black')
ax.plot(fadet.getTable())
# plt.show()

s.gui(locals())
