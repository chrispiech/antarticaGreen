import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import colorsys
import random

RADIUS = 0.5

def main():
	rgb = np.load(open('rgb.npy'))

	

	colors = getColors(rgb)

	showGB (colors)

def showGB(colors):
	done = 0.0
	for color in colors:
		done += 1
		if done % 1000 == 0: print done / len(colors)
		if random.random() > 0.33: continue
		plt.scatter(color[1], color[2], color = color)
	plt.xlabel('Green')
	plt.ylabel('Blue')
	plt.xlim([0.0,1.0])
	plt.ylim([0.0,1.0])
	plt.show()

def showRgb(colors):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	done = 0.0
	for color in colors:
		done += 1
		if done % 1000 == 0: print done / len(colors)
		if random.random() > 0.05: continue
		ax.scatter(color[1], color[2], color[0], color = color)
	ax.set_xlabel('Green')
	ax.set_ylabel('Blue')
	ax.set_zlabel('Red')
	plt.show()


def showHsv(colors):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	done = 0.0
	for color in colors:
		done += 1
		if done % 1000 == 0: print done / len(colors)
		if random.random() > 0.05: continue
		(h, s, v) = colorsys.rgb_to_hsv(color[0], color[1], color[2])
		ax.scatter(h, s, v, color = color)
	ax.set_xlabel('Hue')
	ax.set_ylabel('Saturation')
	ax.set_zlabel('Value')
	plt.show()

def displayColors(colors):
	done = 0.0
	for color in colors:
		if 2 * color[1] - color[0] - color[2] < 0.07:
			if random.random() > 0.2: continue
			(h, s, v) = colorsys.rgb_to_hsv(color[0], color[1], color[2])

			# The radius is given by the intensity of the color, which is in slot 1. */
			radius = RADIUS * s;
			
			# The angle is given by the hue of the color, which is in slot 0. */
			theta = h * math.pi * 2.0;
			
			# Determine the x and y coordinates. */
			x = 0.5 + radius * math.cos(theta);
			y = 0.5 - radius * math.sin(theta);
			plt.scatter(x, y, color = color)
		done += 1
		if done % 100 == 0: print done / len(colors)
	plt.show()
	

def isLegit(r, g, b):
	if math.isnan(r): return False
	if math.isnan(g): return False
	if math.isnan(b): return False
	return True

def getColors(rgb):
	colors = []
	for row in range(rgb.shape[0]):
		for col in range(rgb.shape[1]):
			red = rgb[row][col][0]
			green = rgb[row][col][1]
			blue = rgb[row][col][2]
			if isLegit(red, green, blue):
				colors.append((red, green, blue))
	return colors


if __name__ == '__main__':
	main()