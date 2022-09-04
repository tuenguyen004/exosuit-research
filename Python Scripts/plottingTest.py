# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import matplotlib.pyplot as plt
import random

time = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
position = []  # This is a List (don't use Array because we need
# need to from numpy import array)
for i in range(len(time)):
    position.append(random.randint(0, 1001))

plt.plot(time, position)
plt.xlabel("Time (hr)")
plt.ylabel("Position (km)")
plt.show()