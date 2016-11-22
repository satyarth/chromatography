# Usage

Import the `Chromatography` class, instantiate it (via a path to an image or PIL Image object), use the `get_palette` or `get_highlights` methods to get what you want.

## Example:

```
from chromatography import Chromatography

palette = Chromatography("image.jpg").get_palette(5)
```

or...


```
from PIL import Image
from chromatography import Chromatography

img = Image("image.jpg")
palette = Chromatography(img).get_palette(5)

```

For example, image/palette:

![source](http://ia800902.us.archive.org/34/items/mbid-4695eb48-98bd-411f-8dd1-f0290a106cd2/mbid-4695eb48-98bd-411f-8dd1-f0290a106cd2-4765009935.jpg) ![result](http://i.imgur.com/vy3YPIb.png)