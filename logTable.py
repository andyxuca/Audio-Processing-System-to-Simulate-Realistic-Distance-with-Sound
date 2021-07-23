from pyo import *
import matplotlib.pyplot as plt
import math as math

#function for Log Amplitude
def amp(dist):
    return -0.231588*math.log(dist) + 0.970437

#Boot and Start pyo server
s = Server().boot().start()
print('Server Booted')

# sound path
snd_path = 'sound path'

# Takes User input for distance
dist = int(input('Enter a distance: '))

# Fills a list with amplitude multipliers based on input distance
logTableList = []
counter = 0
for i in range(dist, 66):
    logTableList.append((counter, amp(i)))
    counter += 1

# Create LogTable with logTableList
t = LogTable(logTableList)

# Visual Plot of LogTable
fig,ax = plt.subplots()
plt.xlim(0, 66)
ax.grid(color='black')
ax.plot(t.getTable())
plt.show()




