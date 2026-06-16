"""
core/constants.py
Change sizes here — nothing else needs touching.
All units: millimetres.
"""

# Wall & structural 
WALL_T      = 200       # wall thickness
MARGIN      = 1000      # inner margin: equipment to outer wall (sides/rear)

# Transformer clearances    
TX_MIN_WALL_CLEARANCE   = 1000   # transformer to side wall
TX_MIN_REAR_CLEARANCE   = 1000   # transformer to rear wall (top)
TX_MIN_FRONT_CLEARANCE  = 1500   # transformer to front (towards LT panel)
TX_MIN_BETWEEN          = 1500   # gap between adjacent transformers

# HT Panel clearances
HT_MIN_FRONT_CLEARANCE  = 2000   # front aisle (towards LT panel)
HT_MIN_REAR_CLEARANCE   = 1000   # rear wall / cable duct
HT_MIN_SIDE_CLEARANCE   = 1000   # end walls

# LT panel clearances 
LT_MIN_FRONT_CLEARANCE  = 1500   # aisle below LT towards DG row
LT_MIN_REAR_CLEARANCE   = 800    # gap above LT (towards TX row)
LT_MIN_SIDE_CLEARANCE   = 750    # LT to side walls

# DG synchronizer clearances 
DGS_MIN_FRONT_CLEARANCE = 3000   # maintenance aisle at front
DGS_MIN_WALL_CLEARANCE  = 1500   # to side walls
DGS_MIN_REAR_CLEARANCE  = 1500   # to rear wall

# NGR clearances 
NGR_GAP                 = 1000   # NGR to adjacent equipment / wall
TX_NGR_SPACING          = 1000   # min gap: TX-last ↔ TX NGR, and TX NGR ↔ HT Room

# Aisle widths
MIN_MAINTENANCE_AISLE   = 1500
MIN_CABLE_AISLE         = 1000

# Minimum room areas
MIN_CONTROL_ROOM_AREA   = 12_000_000  # mm²
MIN_SCADA_ROOM_AREA     =  9_000_000
MIN_UPS_ROOM_AREA       = 12_000_000
MIN_TOILET_AREA         =  4_000_000

# Ancillary rooms (fixed) 
ANCILLARY_ROOMS = [
    ("UPS & BATTERY ROOM",         3500, 4000),
    ("SCADA ROOM",                 3500, 4000),
    ("MAINTENANCE & CONTROL ROOM", 3500, 4400),
    ("TOILET",                     3500, 1600),
]
ANCIL_W = ANCILLARY_ROOMS[0][1]   # all same width = 3500

# Transformer block
TX_SIZE   = 3000    # square side
TX_PIN_H  = 300     # bushing pin height above block
TX_PIN_W  = 160     # bushing pin width
TX_PINS   = 3       # number of pins per transformer

# HT Panel 
HT_W = 3000
HT_H = 2000

# HT Separation Room
HT_ROOM_CLEAR_SIDE = HT_MIN_SIDE_CLEARANCE    # 1000 left & right
HT_ROOM_CLEAR_TB   = HT_MIN_REAR_CLEARANCE    # 1000 top & bottom (use rear as conservative)
HT_ROOM_CLEAR_FRONT = HT_MIN_FRONT_CLEARANCE  # 2000 front aisle
HT_ROOM_WALL_T     = 200    # separation room wall thickness

# LT Panel
LT_H = 1800         # height; width computed to span full equipment row

# NGR blocks
NGR_W = 1200
NGR_H = 1200

# DG Synchronizer
DGS_W_DEFAULT = 4000
DGS_H_DEFAULT = 2500

# DG Day Tank 
DAYTANK_W = 2000
DAYTANK_H = 2000

# APFC Panel 
APFC_W = 2500
APFC_H = 1800

# Entrance 
ENTRANCE_H       = 1500
ENTRANCE_CHEV    = 600

# Text heights 
TH_LARGE  = 350
TH_NORMAL = 220
TH_SMALL  = 160
TH_TINY   = 130

# Title block 
TITLE_BLOCK_H = 1500
TITLE_OFFSET  = 600
