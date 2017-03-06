import gdal
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random
import math
import colorsys

COLOR_NAN = -28672

def main():
	ds = gdal.Open('test.tif')
	cloudBand = ds.GetRasterBand(1)
	redBand = ds.GetRasterBand(2)
	blueBand = ds.GetRasterBand(3)
	greenBand = ds.GetRasterBand(4)
	cloudArray = cloudBand.ReadAsArray()

	redArray = redBand.ReadAsArray()
	blueArray = blueBand.ReadAsArray()
	greenArray = greenBand.ReadAsArray()
	

	preProcess(cloudArray, redArray, greenArray, blueArray)
	rgbImage = makeRGBFast(redArray, greenArray, blueArray)

	applyHansRule(rgbImage)

	#np.save(open('rgb', 'w'), rgbImage)
	#'saved'

	plotImg(rgbImage)
	#testFn(rgbImage)
	#showHsv(rgbImage)

def applyHansRule(rgbImage):
	for r in range(rgbImage.shape[0]):
		for c in range(rgbImage.shape[1]):
			red = rgbImage[r][c][0]
			green = rgbImage[r][c][1]
			blue = rgbImage[r][c][2]
			hans = 2 * green - red - blue
			if hans > 0.07:
				rgbImage[r][c][0] = 1.0
				rgbImage[r][c][1] = 0.0
				rgbImage[r][c][2] = 0.0
			

def showHsv(rgbImage):
	hs = []
	ss = []
	vs = []
	for r in range(rgbImage.shape[0]):
		for c in range(rgbImage.shape[1]):
			red = rgbImage[r][c][0]
			green = rgbImage[r][c][1]
			blue = rgbImage[r][c][2]
			if isUsed(red, green, blue):
				(h, s, v) = colorsys.rgb_to_hsv(red, green, blue)
				hs.append(h)
				ss.append(s)
				vs.append(v)
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(hs,ss, vs)
	ax.set_xlabel('Hue')
	ax.set_ylabel('Saturation')
	ax.set_zlabel('Value')
	plt.show()

def testFn(rgbImage):
	values = []
	for r in range(rgbImage.shape[0]):
		for c in range(rgbImage.shape[1]):
			red = rgbImage[r][c][0]
			green = rgbImage[r][c][1]
			blue = rgbImage[r][c][2]
			if isUsed(red, green, blue):
				value = 2 * green - red - blue
				values.append(value)
	h = np.histogram(values)
	for i in range(len(h[0])):
		print h[0][i], h[1][i]


def isUsed(r, g, b):
	if math.isnan(r): return False
	if math.isnan(g): return False
	if math.isnan(b): return False
	return True

def showRgb(rgbImage):
	print 'show rgb...'
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	xs = []
	ys = []
	zs = []
	for r in range(rgbImage.shape[0]):
		for c in range(rgbImage.shape[1]):
			if(random.random() < 0.1):
				red = rgbImage[r][c][0]
				green = rgbImage[r][c][1]
				blue = rgbImage[r][c][2]
				if isUsed(red, green, blue):
					xs.append(red) 
					ys.append(green) 
					zs.append(blue) 
	ax.scatter(xs, ys, zs)
	ax.set_xlabel('Red')
	ax.set_ylabel('Green')
	ax.set_zlabel('Blue')
	plt.show()
	
def plotImg(rgbImage):
	imgplot = plt.imshow(rgbImage)
	plt.show()

def normalize(pixelValue):
	if pixelValue == COLOR_NAN:
		return float('nan')
	if pixelValue < 0:
		return 0.0
	if pixelValue > 10000:
		return 1.0
	return pixelValue / 10000.0

def makeRGB(red, green, blue):
	print 'making rgb...'
	pixels = np.zeros((red.shape[0], red.shape[1], 3))
	for r in range(red.shape[0]):
		for c in range(red.shape[1]):
			pixels[r][c][0] = normalize(red[r][c])
			pixels[r][c][1] = normalize(green[r][c])
			pixels[r][c][2] = normalize(blue[r][c])
	return pixels

def makeRGBFast(red, green, blue):
	print 'making rgb...'
	pixels = np.zeros((red.shape[0], red.shape[1], 3))
	pixels[:,:,0] = red
	pixels[:,:,1] = green
	pixels[:,:,2] = blue
	isNan = pixels == COLOR_NAN
	isUnderflow = pixels < 0.0
	isOverflow = pixels > 10000.0
	pixels[isUnderflow] = 0.0
	pixels[isOverflow] = 10000.0
	pixels[isNan] = float('nan')
	return pixels / 10000.0

def preProcess(cloud, red, green, blue):
	print 'pre processing...'
	for r in range(cloud.shape[0]):
		for c in range(cloud.shape[1]):
			value = cloud[r][c]
			#print "{0:b}".format(value)
			bitStream = bin(value)[2:]
			cloudBits = bitStream[-2:]
			landBits = bitStream[-6:-3]
			isLand = landBits == '001'
			isClear = cloudBits == '00'
			if not isClear:
				red[r][c] = COLOR_NAN
				green[r][c] = COLOR_NAN
				blue[r][c] = COLOR_NAN
			if isLand:
				red[r][c] = COLOR_NAN
				green[r][c] = COLOR_NAN
				blue[r][c] = COLOR_NAN



			

if __name__ == '__main__':
	main()
