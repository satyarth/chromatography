from chromatography import Chromatography
import svgwrite
from colorsys import rgb_to_hsv

def valid_pixel(pixel):
	if rgb_to_hsv(pixel[0]/255, pixel[1]/255, pixel[2]/255)[1] + rgb_to_hsv(pixel[0]/255, pixel[1]/255, pixel[2]/255)[2] < 1.2:
		return False
	return True

c = Chromatography("test.jpg")
palette = c.get_palette(5, valid_pixel)

def render_palette(centroids):
	dwg = svgwrite.Drawing("out.svg",
							profile='full',
							size=(480, 480))
	for i in range(len(palette)):
		dwg.add(dwg.rect(insert=(0, i*480/len(palette)), size=(480, 480/len(palette)), rx=None, ry=None, fill='rgb'+str(centroids[i])))
	dwg.save()

render_palette(palette)