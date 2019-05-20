#
# RCTF2019 - printer (misc)
#
# Thank tangerine1202 for helping me write this script to draw the graph
# Credit to tangerine1202 
# tangerine1202's github: https://github.com/tangerine1202
#

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


fig = plt.figure()
ax = fig.add_subplot(111,  aspect='equal')
plt.xticks(range(0, 500, 100))
plt.yticks(range(-500, 0, 100))

import os
print os.getcwd()
with open('./bar', 'r') as _file:

	params_ls = np.array([0, 0, 0 ,0])
	for ls in _file:
		ls = np.array( ls.split(', ') )
		ls = ls.astype(np.int)
		ls[1] = -ls[1]
		ls[3] = -ls[3]
		params_ls = np.vstack( (params_ls, ls) )

	for params in params_ls:
		ax.add_patch(
		    patches.Rectangle(
		        (params[0], params[1]),   # (x,y)
		        params[2],          # width
		        params[3],          # height
		    )
		)

# BITMAP 138,75,   26,48,1,
with open('./leftover.bin', 'r') as _file:
	_L = 138
	_R = 75

	s = _file.read(9984)
        # print(s)
	s = np.array(list(s)).reshape((-1, 208))

	for i in range(s.shape[0]):
		for j in range(s.shape[1]):
			if s[i][j] == '1':
				ax.add_patch(
					patches.Rectangle( ( _L+j, -(_R+i) ), 1, 1)
				) 
plt.show()


