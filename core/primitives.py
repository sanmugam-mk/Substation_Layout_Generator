"""
core/primitives.py
Low-level drawing helpers.
This file only knows how to draw shapes 
"""

from ezdxf.enums import TextEntityAlignment


def rect(msp, x, y, w, h, layer):
    """Draw a closed rectangle. Origin = bottom-left."""
    pts = [(x, y), (x+w, y), (x+w, y+h), (x, y+h), (x, y)]
    msp.add_lwpolyline(pts, dxfattribs={"layer": layer, "closed": True})


def inner_rect(msp, x, y, w, h, layer, pad_frac=0.12):
    """Draw a rectangle inset by pad_frac on each side (block symbol)."""
    px = w * pad_frac
    py = h * pad_frac
    rect(msp, x + px, y + py, w - 2*px, h - 2*py, layer)


def line(msp, x1, y1, x2, y2, layer, linetype=None):
    attrs = {"layer": layer}
    if linetype:
        attrs["linetype"] = linetype
    msp.add_line((x1, y1), (x2, y2), dxfattribs=attrs)


def text_center(msp, cx, cy, content, height, layer):
    """Add text centred on (cx, cy)."""
    t = msp.add_text(content, dxfattribs={"layer": layer, "height": height})
    t.set_placement((cx, cy), align=TextEntityAlignment.MIDDLE_CENTER)


def text_at(msp, x, y, content, height, layer, align="LEFT"):
    t = msp.add_text(content, dxfattribs={"layer": layer, "height": height})
    t.set_placement((x, y), align=TextEntityAlignment[align])


def dim_horizontal(msp, x1, x2, y, drop, layer):
    """Horizontal linear dimension placed `drop` mm below y."""
    try:
        msp.add_linear_dim(
            base=(x1, y - drop),
            p1=(x1, y), p2=(x2, y),
            angle=0,
            override={"dimtxt": 250, "dimasz": 200},
            dxfattribs={"layer": layer},
        ).render()
    except Exception:
        pass


def dim_vertical(msp, x, y1, y2, offset, layer):
    """Vertical linear dimension placed `offset` mm to the right of x."""
    try:
        msp.add_linear_dim(
            base=(x + offset, y1),
            p1=(x, y1), p2=(x, y2),
            angle=90,
            override={"dimtxt": 250, "dimasz": 200},
            dxfattribs={"layer": layer},
        ).render()
    except Exception:
        pass
