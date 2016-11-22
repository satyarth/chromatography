from PIL import Image
from random import sample
from colorsys import rgb_to_hsv

class InputError(Exception):
	pass

class ChromatographyException(Exception):
	pass

class NotEnoughValidPixels(ChromatographyException):
	pass

class MalformedImage(ChromatographyException):
	pass

def sq_euclidian_distance(pixel1, pixel2):
	return sum([(pixel1[i]-pixel2[i])**2 for i in [0, 1, 2]])

def bright_pixel(pixel):
	(h, s, v) = rgb_to_hsv(pixel[0]/255, pixel[1]/255, pixel[2]/255)
	if s + v > 1.4:
		return True
	return False

class Cluster(object):
	def __init__(self, centroid):
		self.centroid = centroid
		self.pixels = [centroid]

	def get_mean(self):
		mean_value = tuple([int(sum(x)/len(self.pixels)) for x in zip(*self.pixels)])
		return mean_value

	def size(self):
		return len(self.pixels)


class Chromatography(object):
	def __init__(self, img):
		if isinstance(img, Image.Image): # Input is a instance of the PIL Image class
			self.img = img
			
		elif isinstance(img, str):	# Input is a string pointing to an image file
			self.img = Image.open(img)

		else:
			raise InputError("Argument must be an instance of PIL's Image class or the path to an image")

		self.scale_image()
		
	def scale_image(self):
		(height, width) = self.img.size
		target_area = 10000
		if height * width > target_area:
			ratio = (height*width/target_area)
			self.img = self.img.resize((int(height/ratio), int(width/ratio)), Image.ANTIALIAS)

	def get_palette(self, k=4, filter_pixels=None):
		all_pixels = list(self.img.getdata())
		try:
			self.pixels = list(filter(filter_pixels, all_pixels))
		except TypeError:
			raise MalformedImage
		# TODO: Pick the initial centroids in a better way
		try:
			centroids = sample(self.pixels, k)
		# Not enough pixels to sample the initial centroids from
		except ValueError:
			raise NotEnoughValidPixels

		while True:
			new_centroids = self.new_centroids(centroids)
			if sum([sq_euclidian_distance(a, b) for (a, b) in zip(centroids, new_centroids)]) < 10:
				break
			centroids = new_centroids
		centroids = self.sort_centroids(centroids)
		return centroids

	def get_highlights(self, k=4, filter_pixels=None):
		palette = self.get_palette(k*2, filter_pixels)
		highlights = self.sort_centroids(palette)[k:2*k]
		return list(reversed(highlights))

	def sort_centroids(self, centroids):
		clusters = [Cluster(c) for c in centroids]
		sorted_clusters = sorted(clusters, key=lambda c: sum([sq_euclidian_distance(c.centroid, centroid)*c.size() for centroid in centroids]))
		return [c.centroid for c in sorted_clusters]

	def new_centroids(self, centroids):
		clusters = [Cluster(centroid) for centroid in centroids]
		for pixel in self.pixels:
			min(clusters, key=lambda c: sq_euclidian_distance(pixel, c.centroid)).pixels.append(pixel)
		return [c.get_mean() for c in clusters]

	