from centrifuge import Centrifuge
import svgwrite

c = Centrifuge("test.jpg")
palette = c.get_palette(4)

def render_palette(centroids):
	dwg = svgwrite.Drawing("out.svg",
							profile='full',
							size=(480, 480))
	for i in range(len(palette)):
		dwg.add(dwg.rect(insert=(0, i*480/len(palette)), size=(480, 480/len(palette)), rx=None, ry=None, fill='rgb'+str(centroids[i])))
	dwg.save()

render_palette(palette)