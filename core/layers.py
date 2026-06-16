"""
core/layers.py
All DXF layer definitions.
Format: { layer_name: (aci_color, lineweight_in_hundredths) }

ACI colour reference (AutoCAD Color Index):
  1=red  2=yellow  3=green  4=cyan  5=blue  6=magenta  7=white/black  8=grey
"""

LAYER_DEFS = {
    "WALLS":        (7,  50),
    "ROOMS":        (6,  25),   # magenta — ancillary rooms
    "TRANSFORMERS": (2,  25),   # yellow
    "HT_PANEL":     (1,  25),   # red
    "HT_ROOM":      (1,  35),   # red, heavier — HT separation room walls
    "BACKGROUND":   (0,   1),   # color 0 = ByBlock (used for door-gap override)
    "LT_PANEL":     (4,  25),   # cyan
    "DG":           (3,  25),   # green
    "NGR":          (2,  18),   # yellow
    "APFC":         (4,  18),   # cyan
    "ANNOTATIONS":  (7,  13),
    "DIMENSIONS":   (7,  13),
    "TITLE_BLOCK":  (7,  35),
    "NORTH":        (7,  18),
    "ENTRANCE":     (7,  18),
}


def register_layers(doc):
    """Add all layers to an ezdxf document."""
    for name, (color, lw) in LAYER_DEFS.items():
        if name not in doc.layers:
            doc.layers.new(name, dxfattribs={"color": color, "lineweight": lw})
