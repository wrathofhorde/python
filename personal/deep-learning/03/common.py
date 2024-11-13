import func
import numpy as np
import matplotlib.pylab as plt

x = np.arange(-5, 5, 0.1)
y1 = func.step(x)
y2 = func.sigmoid(x)

plt.plot(x, y1)
plt.plot(x, y2)
plt.ylim(-0.1, 1.2)
plt.show()
