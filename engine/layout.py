"""
engine/layout.py
This file decides where the each blocks should go, and how big the canvas should be.

Order of blocks placed inside the main room:
  ROW 0  TX-1…TX-n + TX-NGR-n…TX-NGR-1 + HT PANEL WITH CLEARANCE ROOM (top)
  ROW 1  LT PANEL          
  ROW 2  DG SYNCHRONIZER + APFCRs (bottom)

Key clearance rules enforced:
  TX ↔ TX              = TX_MIN_BETWEEN         (1500)
  TX to top wall       = TX_MIN_REAR_CLEARANCE   (1000)
  TX-last ↔ TX NGR-n   = TX_NGR_SPACING          (1000)
  TX NGR-1 right wall  = HT Room left wall (shared, zero gap)
  HT-room bottom → LT top  = HT_MIN_FRONT_CLEARANCE (2000)
  LT to side walls     = LT_MIN_SIDE_CLEARANCE   (750)
  LT bottom → DG top   = DGS_MIN_REAR_CLEARANCE  (1500)
  DG front aisle       = MIN_MAINTENANCE_AISLE   (1500)
"""

from dataclasses import dataclass, field
from typing import List, Tuple

from core.constants import (
    WALL_T,
    ANCILLARY_ROOMS, ANCIL_W,

    TX_PIN_H,
    TX_MIN_WALL_CLEARANCE, TX_MIN_REAR_CLEARANCE,
    TX_MIN_BETWEEN,

    HT_W, HT_H,
    HT_ROOM_CLEAR_SIDE, HT_ROOM_CLEAR_TB, HT_ROOM_CLEAR_FRONT,
    HT_MIN_FRONT_CLEARANCE,
    HT_ROOM_WALL_T,

    LT_MIN_SIDE_CLEARANCE,

    TX_NGR_SPACING,

    DGS_MIN_FRONT_CLEARANCE, DGS_MIN_WALL_CLEARANCE, DGS_MIN_REAR_CLEARANCE,
    MIN_MAINTENANCE_AISLE,

    ENTRANCE_H,
)

@dataclass
class Box:
    """Positioned rectangle. Origin (x,y) = bottom-left. All mm."""
    x: float; y: float; w: float; h: float

    @property
    def cx(self):    return self.x + self.w / 2
    @property
    def cy(self):    return self.y + self.h / 2
    @property
    def top(self):   return self.y + self.h
    @property
    def right(self): return self.x + self.w


@dataclass
class LayoutResult:
    canvas_w: float = 0
    canvas_h: float = 0

    ancil_rooms:   List[Tuple[str, 'Box']] = field(default_factory=list)
    main:          'Box' = None

    transformers:  List['Box'] = field(default_factory=list)
    ht_panel:      'Box' = None
    ht_room:       'Box' = None
    lt_panel:      'Box' = None
    tx_ngrs:       List['Box'] = field(default_factory=list)  # all TX NGR boxes
    tx_ngr:        'Box' = None   # first (rightmost) NGR — backward compat
    dg_ngr:        'Box' = None
    dg_sync:       'Box' = None
    apfc_panels:   List['Box'] = field(default_factory=list)
    shutter_y:    float = 0
    entrance_cx:  float = 0
    entrance_y:   float = 0


def compute_layout(p) -> LayoutResult:
    L = LayoutResult()

    DGS_W = p.dg_sync_length   # horizontal (X)
    DGS_H = p.dg_sync_width    # vertical   (Y)

    # User-supplied NGR / APFC dimensions
    NGR_W = p.tx_ngr_length
    NGR_H = p.tx_ngr_width
    APFC_W = p.apfc_length
    APFC_H = p.apfc_width

    # User-supplied transformer dimensions
    TX_W = p.tx_length   # horizontal (X)
    TX_H = p.tx_width    # vertical   (Y)

    # User-supplied LT panel dimensions
    LT_W = p.lt_panel_length   # horizontal (X)
    LT_H = p.lt_panel_width    # vertical   (Y)

    # Number of TX NGRs (0 = none)
    n_ngr = max(0, int(p.n_tx_ngr))

    # 1. Ancillary column 
    ancil_total_h = sum(r[2] for r in ANCILLARY_ROOMS)

    # 2. ROW 0 geometry 
    tx_row_w = p.n_tx * TX_W + (p.n_tx - 1) * TX_MIN_BETWEEN

    # TX NGR slot: TX-last ←1000→ [NGR-n … NGR-1] | HT Room
    # All NGRs packed side by side; rightmost shares HT room outer wall.
    if n_ngr > 0:
        tx_ngr_slot_w = TX_NGR_SPACING + NGR_W   # only 1 unit wide — stacked vertically
    else:
        tx_ngr_slot_w = TX_MIN_BETWEEN

    HT_W = p.ht_panel_length
    HT_H = p.ht_panel_width

    ht_room_w = HT_W + 2 * HT_ROOM_CLEAR_SIDE + 2 * HT_ROOM_WALL_T
    ht_room_h = HT_H + HT_ROOM_CLEAR_TB + HT_ROOM_CLEAR_FRONT + 2 * HT_ROOM_WALL_T

    row0_h = max(TX_H + TX_PIN_H, ht_room_h)
    row0_w = tx_row_w + tx_ngr_slot_w + ht_room_w

    # 3. ROW 1: LT Panel 
    # (size now comes directly from user input: p.lt_panel_length / width)

    # 4. ROW 2: DG Synchronizer + APFCRs 
    n_apfcr     = p.n_tx if p.has_apfc else 0
    apfcr_row_w = n_apfcr * APFC_W + max(0, n_apfcr - 1) * DGS_MIN_WALL_CLEARANCE
    dg_row_w    = DGS_W + (DGS_MIN_WALL_CLEARANCE + apfcr_row_w if n_apfcr else 0)
    dg_row_h    = max(DGS_H, APFC_H if p.has_apfc else 0)

    # 5. Main inner width
    side_margin  = max(TX_MIN_WALL_CLEARANCE, LT_MIN_SIDE_CLEARANCE, DGS_MIN_WALL_CLEARANCE)
    equip_w      = max(row0_w, dg_row_w, LT_W)
    main_inner_w = equip_w + 2 * side_margin

    # 6. Main inner height 
    rows_h = (
        TX_MIN_REAR_CLEARANCE           # 1000
        + row0_h
        + HT_MIN_FRONT_CLEARANCE        # 2000
        + LT_H                          # user-supplied LT panel width (Y)
        + DGS_MIN_REAR_CLEARANCE        # 1500
        + dg_row_h
        + MIN_MAINTENANCE_AISLE         # 1500
    )
    main_inner_h = rows_h

    # 7. Canvas 
    total_h = max(ancil_total_h, main_inner_h) + 2 * WALL_T
    total_w = WALL_T + ANCIL_W + WALL_T + main_inner_w + WALL_T

    L.canvas_w = total_w
    L.canvas_h = total_h

    # 8. Origins
    main_x = WALL_T + ANCIL_W + WALL_T
    main_y = WALL_T
    L.main = Box(main_x, main_y, main_inner_w, total_h - 2 * WALL_T)

    # 9. Ancillary rooms (top → bottom)
    ry = main_y + (total_h - 2 * WALL_T)
    for name, rw, rh in ANCILLARY_ROOMS:
        ry -= rh
        L.ancil_rooms.append((name, Box(WALL_T, ry, rw, rh)))

    # 10. Y positions 
    top_inner_y  = main_y + (total_h - 2 * WALL_T)
    tx_pin_top_y = top_inner_y - TX_MIN_REAR_CLEARANCE
    tx_y         = tx_pin_top_y - TX_PIN_H - TX_H

    # HT room shares the TOP wall with the main room (top-right corner)
    ht_room_y     = top_inner_y - ht_room_h
    row0_bottom_y = min(tx_y, ht_room_y)

    lt_y      = row0_bottom_y - HT_MIN_FRONT_CLEARANCE - LT_H
    lt_w      = LT_W
    dg_sync_y = lt_y - DGS_MIN_REAR_CLEARANCE - dg_row_h

    # 11. X positions
    equip_start_x = main_x + side_margin

    for i in range(p.n_tx):
        tx_x = equip_start_x + i * (TX_W + TX_MIN_BETWEEN)
        L.transformers.append(Box(tx_x, tx_y, TX_W, TX_H))

    # HT room shares the RIGHT wall with the main room (top-right corner)
    ht_room_x = main_x + main_inner_w - ht_room_w

    # TX NGRs: stacked vertically, all touching HT room outer (left) wall
    # NGR-1 at top, NGR-n at bottom, centered within HT room height
    if n_ngr > 0:
        ngr_x         = ht_room_x - NGR_W   # shared wall with HT room
        total_ngr_h   = n_ngr * NGR_H
        ngr_stack_y   = ht_room_y + (ht_room_h - total_ngr_h) // 2  # vertically centred in HT room
        for i in range(n_ngr):
            ny = ngr_stack_y + i * NGR_H
            L.tx_ngrs.append(Box(ngr_x, ny, NGR_W, NGR_H))
        L.tx_ngr = L.tx_ngrs[0]   # backward compat

    L.ht_room  = Box(ht_room_x, ht_room_y, ht_room_w, ht_room_h)
    L.ht_panel = Box(
        ht_room_x + HT_ROOM_WALL_T + HT_ROOM_CLEAR_SIDE,
        ht_room_y + HT_ROOM_WALL_T + HT_ROOM_CLEAR_FRONT,
        HT_W, HT_H
    )

    L.lt_panel = Box(main_x + LT_MIN_SIDE_CLEARANCE, lt_y, lt_w, LT_H)
    L.dg_sync  = Box(equip_start_x, dg_sync_y, DGS_W, DGS_H)

    if p.has_apfc:
        apfc_cursor = equip_start_x + DGS_W + DGS_MIN_WALL_CLEARANCE
        apfc_y      = dg_sync_y + (dg_row_h - APFC_H) // 2
        for i in range(n_apfcr):
            L.apfc_panels.append(Box(apfc_cursor, apfc_y, APFC_W, APFC_H))
            apfc_cursor += APFC_W + DGS_MIN_WALL_CLEARANCE

    # 12. Shutter & entrance
    L.shutter_y   = top_inner_y
    L.entrance_cx = main_x + main_inner_w / 2
    L.entrance_y  = main_y + ENTRANCE_H / 2

    return L