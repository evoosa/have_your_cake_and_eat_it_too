
# Design

## Camera Service
- run with `python eyes.py`
- capture images, dump to `cur.png` and register last eyes to `lasteyes.txt`
- save the first eyes in every <interval> seconds to `faces/<timestamp>.png` (for later analysis)

## HTML Server
- run with `flask --app seducer.py run --host=0.0.0.0`
- for starters present last seen eyes status and image
- `localhost:5000/first.html`
- `localhost:5000/gallery.html`
- `localhost:5000/cur.png`