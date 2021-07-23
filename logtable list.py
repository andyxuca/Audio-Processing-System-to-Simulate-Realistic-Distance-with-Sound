from pyo import *
import matplotlib.pyplot as plt
import math as math

def amp(dist):
    return -0.231588*math.log(dist) + 0.970437

s = Server().boot().start()
print('Server Booted')

# sound path
snd_path = 'sound path'

dist = int(input('Enter a distance: '))

logTableList = []
counter = 0
for i in range(dist, 66):
    logTableList.append((counter, amp(i)))
    counter += 1
print(logTableList)

t = LogTable(logTableList)

fig,ax = plt.subplots()
plt.xlim(0, 66)
ax.grid(color='black')
ax.plot(t.getTable())
plt.show()




