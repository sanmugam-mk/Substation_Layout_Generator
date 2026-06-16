"""
output/dxf_writer.py
====================
Assembles the final DXF document.
Calls layout engine → placer → saves file.
This is the only file that imports ezdxf directly.
"""

import ezdxf
import os
from core.layers import register_layers
from engine.layout import compute_layout
from engine.placer import (
    draw_outer_walls, draw_ancil_divider, draw_ancil_rooms,
    draw_north_arrow, draw_perforated_shutter, draw_entrance,
    draw_title_block, draw_overall_dims,
    draw_transformer, draw_ht_room, draw_lt_panel,
    draw_ngr, draw_dg_sync, draw_apfc,
)


def write_dxf(p, output_dir=None) -> str:
    if output_dir is None:
        output_dir = os.getcwd()

    doc = ezdxf.new(dxfversion="R2010")
    doc.header["$INSUNITS"] = 4   # mm
    doc.header["$LUNITS"]   = 2   # decimal

    register_layers(doc)

    if "DASHED" not in doc.linetypes:
        doc.linetypes.new(
            "DASHED",
            dxfattribs={"description": "Dashed", "pattern": [6.0, 3.0, -3.0]},
        )

    msp = doc.modelspace()

    # ── Compute layout ────────────────────────────────────────
    L = compute_layout(p)
    p.canvas_w = int(L.canvas_w)
    p.canvas_h = int(L.canvas_h)

    # ── Structural elements ───────────────────────────────────
    draw_outer_walls(msp, L)
    draw_ancil_divider(msp, L)
    draw_ancil_rooms(msp, L)
    draw_north_arrow(msp, L)
    draw_perforated_shutter(msp, L, p)
    draw_entrance(msp, L)
    draw_title_block(msp, L, p)
    draw_overall_dims(msp, L)

    # ── ROW 0: Transformers + HT Separation Room ─────────────
    for i, b in enumerate(L.transformers):
        draw_transformer(msp, b, f"TX-{i+1}", p.supply_kv)

    draw_ht_room(msp, L.ht_room, L.ht_panel, p.ht_incomers, p.ht_outgoings)

    # ── TX NGRs (placed left of HT room, sharing its outer wall) ─
    n_ngr = len(L.tx_ngrs)
    for i, b in enumerate(L.tx_ngrs):
        label = "TX NGR" if n_ngr == 1 else f"TX NGR-{i + 1}"
        draw_ngr(msp, b, label)

    if L.dg_ngr:
        draw_ngr(msp, L.dg_ngr, "DG NGR")

    # ── ROW 1: LT Panel ───────────────────────────────────────
    draw_lt_panel(msp, L.lt_panel, p.lt_incomers, p.lt_outgoings)

    # ── ROW 2: DG Synchronizer + APFC ────────────────────────
    if L.dg_sync:
        dg_rating_label = f"{p.dg_sync_count}×{p.dg_sync_unit_rating} kVA"
        draw_dg_sync(msp, L.dg_sync, dg_rating_label)

    for i, b in enumerate(L.apfc_panels):
        draw_apfc(msp, b, label=f"APFCR-{i+1}")

    # ── Save ──────────────────────────────────────────────────
    out_path = os.path.join(output_dir, p.out_file)
    doc.saveas(out_path)
    return out_path