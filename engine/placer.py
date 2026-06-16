"""
engine/placer.py

This file draws the blocks at the specified position in the AutoCAD space
geomentry of the blocks - given by  primitives.py file
position of the blocks to be placed - given by layout.py file

Each draw_* function is responsible for exactly one block type.
"""

from core.constants import (
    TX_PIN_H, TX_PIN_W, TX_PINS,
    TH_LARGE, TH_NORMAL, TH_SMALL, TH_TINY,
    WALL_T, ANCIL_W,
    ENTRANCE_CHEV,
    HT_ROOM_WALL_T,
)
from core.primitives import rect, inner_rect, line, text_center, text_at

# STRUCTURAL
def draw_outer_walls(msp, L):
    rect(msp, 0, 0, L.canvas_w, L.canvas_h, "WALLS")

def draw_ancil_divider(msp, L):
    div_x = WALL_T + ANCIL_W
    line(msp, div_x, 0, div_x, L.canvas_h, "WALLS")

def draw_ancil_rooms(msp, L):
    for name, b in L.ancil_rooms:
        rect(msp, b.x, b.y, b.w, b.h, "ROOMS")
        line(msp, b.x, b.top, b.x + b.w, b.top, "ROOMS")
        text_center(msp, b.cx, b.cy + TH_NORMAL * 0.8, name, TH_SMALL, "ROOMS")
        size_str = f"{int(b.w)} × {int(b.h)}"
        text_center(msp, b.cx, b.cy - TH_NORMAL * 0.8, size_str, TH_TINY, "ROOMS")

def draw_north_arrow(msp, L, r=400):
    cx = L.main.x + 600
    cy = L.main.top - 600
    msp.add_circle((cx, cy), r, dxfattribs={"layer": "NORTH"})
    line(msp, cx, cy, cx, cy + r * 1.6, "NORTH")
    text_center(msp, cx, cy + r * 1.95, "N", TH_SMALL, "NORTH")

def draw_perforated_shutter(msp, L, p):
    y  = L.shutter_y
    x0 = L.main.x
    x1 = L.main.right
    line(msp, x0, y, x1, y, "WALLS")
    text_center(msp, (x0 + x1) / 2, y + 350, "PERFORATED ROLLING SHUTTER", TH_SMALL, "ANNOTATIONS")
    n_rx = 3  # fixed — RX labels evenly spaced across shutter
    seg_w = L.main.w / n_rx
    for i in range(n_rx):
        cx = L.main.x + seg_w * i + seg_w / 2
        text_center(msp, cx, y + 700, f"RX-{i+1}", TH_NORMAL, "ANNOTATIONS")

def draw_entrance(msp, L):
    cx = L.entrance_cx
    y  = L.main.y
    line(msp, cx, y + ENTRANCE_CHEV, cx - ENTRANCE_CHEV, y, "ENTRANCE")
    line(msp, cx, y + ENTRANCE_CHEV, cx + ENTRANCE_CHEV, y, "ENTRANCE")
    text_center(msp, cx, y - TH_NORMAL * 1.2, "MAIN ENTRANCE", TH_NORMAL, "ANNOTATIONS")

def draw_title_block(msp, L, p):
    tb_y = 0 - 600 - 1500
    rect(msp, 0, tb_y, L.canvas_w, 1500, "TITLE_BLOCK")
    cx = L.canvas_w / 2
    text_center(msp, cx, tb_y + 1000, "EQUIPMENT LAYOUT PLAN", TH_LARGE, "TITLE_BLOCK")
    sub = f"SUPPLY: {p.supply_kv}kV  |  SCALE: 1:100  |  DIMS IN mm"
    text_center(msp, cx, tb_y + 400, sub, TH_SMALL, "TITLE_BLOCK")


# EQUIPMENT BLOCKS

def draw_transformer(msp, b, label, kv):
    rect(msp, b.x, b.y, b.w, b.h, "TRANSFORMERS")
    inner_rect(msp, b.x, b.y, b.w, b.h, "TRANSFORMERS")
    for frac in [0.25, 0.50, 0.75]:
        px = b.x + b.w * frac
        rect(msp, px - TX_PIN_W/2, b.top, TX_PIN_W, TX_PIN_H, "TRANSFORMERS")
    text_center(msp, b.cx, b.cy + TH_NORMAL * 0.6, label,  TH_NORMAL, "TRANSFORMERS")
    text_center(msp, b.cx, b.cy - TH_NORMAL * 0.8, f"{kv}kV", TH_SMALL, "TRANSFORMERS")

def draw_ht_room(msp, room_box, panel_box, incomers, outgoings):
    """Draw HT separation room walls with door gap, then HT panel centred inside."""
    b  = room_box
    wt = HT_ROOM_WALL_T
    # Outer boundary
    rect(msp, b.x,      b.y,      b.w,           b.h,           "HT_ROOM")
    # Inner boundary (creates visible wall thickness)
    rect(msp, b.x + wt, b.y + wt, b.w - 2 * wt,  b.h - 2 * wt,  "HT_ROOM")
    # Door gap on bottom wall — 1200 wide, centred
    door_w  = 1200
    door_x0 = b.cx - door_w / 2
    door_x1 = b.cx + door_w / 2
    line(msp, door_x0, b.y + wt, door_x1, b.y + wt, "BACKGROUND")
    # Label
    text_center(msp, b.cx, b.top - wt * 2.5, "HT PANEL ROOM", TH_TINY, "HT_ROOM")
    # Panel inside
    draw_ht_panel(msp, panel_box, incomers, outgoings)

def draw_ht_panel(msp, b, incomers, outgoings):
    rect(msp, b.x, b.y, b.w, b.h, "HT_PANEL")
    text_center(msp, b.cx, b.cy + TH_SMALL,       "HT PANEL",                 TH_NORMAL, "HT_PANEL")
    text_center(msp, b.cx, b.cy - TH_SMALL * 1.8, f"({incomers}INCOMER+{outgoings}OUTGOINGS)", TH_TINY, "HT_PANEL")

def draw_lt_panel(msp, b, incomers, outgoings):
    rect(msp, b.x, b.y, b.w, b.h, "LT_PANEL")
    text_center(msp, b.cx, b.cy + TH_SMALL,       "LT PANEL",                          TH_NORMAL, "LT_PANEL")
    text_center(msp, b.cx, b.cy - TH_SMALL * 1.8, f"({incomers}INCOMER + {outgoings}OUTGOINGS)", TH_TINY,   "LT_PANEL")

def draw_ngr(msp, b, label):
    rect(msp, b.x, b.y, b.w, b.h, "NGR")
    text_center(msp, b.cx, b.cy, label, TH_SMALL, "NGR")
    
def draw_dg_sync(msp, b, rating):
    """Single DG Synchronizer panel block."""
    rect(msp, b.x, b.y, b.w, b.h, "DG")
    inner_rect(msp, b.x, b.y, b.w, b.h, "DG", pad_frac=0.06)
    text_center(msp, b.cx, b.cy + TH_NORMAL * 0.8, "DG SYNCHRONIZER", TH_NORMAL, "DG")
    text_center(msp, b.cx, b.cy - TH_NORMAL * 0.4, rating,            TH_SMALL,  "DG")
    # Size annotation inside
    size_str = f"{int(b.w)} × {int(b.h)}"
    text_center(msp, b.cx, b.cy - TH_NORMAL * 1.4, size_str,          TH_TINY,   "DG")

def draw_apfc(msp, b, label="APFC PANEL"):
    rect(msp, b.x, b.y, b.w, b.h, "APFC")
    text_center(msp, b.cx, b.cy, label, TH_NORMAL, "APFC")


# DIMENSIONS
def draw_overall_dims(msp, L):
    from core.primitives import dim_horizontal, dim_vertical
    dim_horizontal(msp, 0, L.canvas_w, 0,          1800, "DIMENSIONS")
    dim_vertical(  msp, L.canvas_w, 0, L.canvas_h, 1800, "DIMENSIONS")
