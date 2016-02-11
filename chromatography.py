from PIL import Image
from random import sample
from colorsys import rgb_to_hsv

class NotEnoughValidPixelsError(Exception):
	pass

def sq_euclidian_distance(pixel1, pixel2):
	return sum([(pixel1[i]-pixel2[i])**2 for i in [0, 1, 2]])

def bright_pixel(pixel):
	(h, s, v) = rgb_to_hsv(pixel[0]/255, pixel[1]/255, pixel[2]/255)
	if s + v > 1.2:
		return True
	return False

class Cluster(object):
	def __init__(self, centroid):
		self.centroid = centroid
		self.pixels = [centroid]

	def get_mean(self):
		mean_value = tuple([int(sum(x)/len(self.pixels)) for x in zip(*self.pixels)])
		return mean_value


class Chromatography(object):
	def __init__(self, image_name):
		self.img = Image.open(image_name)
		self.scale_image()
		
	def scale_image(self):
		# TODO: Figure out a sensible way to scale the image
		self.img = self.img.resize((self.img.size[0]//10, self.img.size[1]//10), Image.ANTIALIAS)

	def get_palette(self, k=4, filter_pixels=None):
		all_pixels = list(self.img.getdata())
		self.pixels = list(filter(filter_pixels, all_pixels))
		# TODO: Pick the initial centroids in a better way
		try:
			centroids = sample(self.pixels, k)
		# Not enough pixels to sample the initial centroids from
		except ValueError:
			raise NotEnoughValidPixelsError

		while True:
			new_centroids = self.new_centroids(centroids)
			if sum([sq_euclidian_distance(a, b) for (a, b) in zip(centroids, new_centroids)]) < 10:
				break
			print(centroids)
			centroids = new_centroids
		# TODO: Sort centroids
		return centroids

	def new_centroids(self, centroids):
		clusters = [Cluster(centroid) for centroid in centroids]
		for pixel in self.pixels:
			min(clusters, key=lambda c: sq_euclidian_distance(pixel, c.centroid)).pixels.append(pixel)
		return [c.get_mean() for c in clusters]

	