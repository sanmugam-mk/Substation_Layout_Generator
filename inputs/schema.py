"""
inputs/schema.py
SubstationParams dataclass.
canvas_w / canvas_h are filled in by the layout engine after compute.

DG Synchronizer dimensions use engineering convention:
  dg_sync_length = horizontal span (X-axis)  — the longer dimension
  dg_sync_width  = vertical depth  (Y-axis)  — the shorter dimension
"""

from dataclasses import dataclass
from core.constants import DGS_W_DEFAULT, DGS_H_DEFAULT, NGR_W, NGR_H, APFC_W, APFC_H, TX_SIZE


@dataclass
class SubstationParams:
    # Power supply 
    supply_kv: int = 22

    # Transformers
    n_tx: int = 3
    tx_rating: str = "1000 kVA"
    tx_length: int = TX_SIZE   # horizontal (X) — per transformer
    tx_width:  int = TX_SIZE   # vertical   (Y) — per transformer

    # HT Panel 
    ht_incomers: int = 1
    ht_outgoings: int = 2
    ht_panel_length: int = 4000
    ht_panel_width: int = 1200

    # LT Panel 
    lt_incomers: int = 1
    lt_outgoings: int = 4
    lt_panel_length: int = 10000
    lt_panel_width: int = 1400

    # DG Synchronizer
    dg_sync_length: int = DGS_W_DEFAULT   # horizontal span (mm)
    dg_sync_width:  int = DGS_H_DEFAULT   # vertical depth  (mm)
    dg_sync_count:       int = 3    # number of DG units  e.g. "3" in "3×500 kVA"
    dg_sync_unit_rating: int = 500  # rating per unit kVA e.g. "500" in "3×500 kVA"

    # Optional blocks 
    has_apfc:  bool = True

    # TX NGR 
    n_tx_ngr:      int = 1       # 0 = none, 1-4 TX NGR units
    tx_ngr_length: int = NGR_W   # horizontal (X) per unit
    tx_ngr_width:  int = NGR_H   # vertical   (Y) per unit

    # APFC Panel dimensions
    apfc_length: int = APFC_W    # horizontal (X), per panel
    apfc_width:  int = APFC_H    # vertical   (Y)

    # Output 
    out_file: str = "substation_layout.dxf"

    # Computed by layout engine 
    canvas_w: int = 0
    canvas_h: int = 0