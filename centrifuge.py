from PIL import Image
from random import sample

def sq_euclidian_distance(pixel1, pixel2):
	return sum([(pixel1[i]-pixel2[i])**2 for i in [0, 1, 2]])

class Cluster(object):
	def __init__(self, centroid):
		self.centroid = centroid
		self.pixels = []

	def get_mean(self):
		# TODO: Less ugly
		r_cum, g_cum, b_cum = 0,0,0
		for pixel in self.pixels:
			r_cum += pixel[0]
			g_cum += pixel[1]
			b_cum += pixel[2]
		total = len(self.pixels)
		mean_value = (r_cum/total, g_cum/total, b_cum/total)
		return min(self.pixels, key=lambda pixel: sq_euclidian_distance(mean_value, pixel))

class Centrifuge(object):
	def __init__(self, image_name):
		self.img = Image.open(image_name)
		self.scale_image()
		self.pixels = list(self.img.getdata())
		
	def scale_image(self):
		# TODO: Figure out a sensible way to scale the image
		self.img = self.img.resize((self.img.size[0]//10, self.img.size[1]//10), Image.ANTIALIAS)

	def get_palette(self, k=4):
		# TODO: Pick the initial centroids in a better way
		centroids = sample(self.pixels, k)
		for i in range(20):
			centroids = self.new_centroids(centroids)
			print(centroids)
		return centroids

	def new_centroids(self, centroids):
		clusters = [Cluster(centroid) for centroid in centroids]
		for pixel in self.pixels:
			min(clusters, key=lambda c: sq_euclidian_distance(pixel, c.centroid)).pixels.append(pixel)
		return [c.get_mean() for c in clusters]

	