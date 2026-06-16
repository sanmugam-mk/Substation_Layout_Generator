"""
inputs/form.py
==============
All user-facing prompts live here.
Returns a fully populated SubstationParams.
"""

from inputs.schema import SubstationParams


# ─────────────────────────────────────────────────────────────
# PROMPT HELPERS
# ─────────────────────────────────────────────────────────────

def _ask_int(prompt: str, default: int) -> int:
    while True:
        raw = input(f"    {prompt} [{default}]: ").strip()
        if raw == "":
            return default
        try:
            val = int(raw)
            if val < 0:
                raise ValueError
            return val
        except ValueError:
            print(f"      ✗  Enter a non-negative integer (or press Enter for {default})")


def _ask_str(prompt: str, default: str) -> str:
    raw = input(f"    {prompt} [{default}]: ").strip()
    return raw if raw else default


def _ask_bool(prompt: str, default: bool) -> bool:
    d = "y" if default else "n"
    while True:
        raw = input(f"    {prompt} (y/n) [{d}]: ").strip().lower()
        if raw == "":
            return default
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("      ✗  Type 'y' or 'n'")


def _section(title: str):
    print(f"\n  ── {title} {'─' * (44 - len(title))}")


# ─────────────────────────────────────────────────────────────
# MAIN FORM
# ─────────────────────────────────────────────────────────────

def collect_inputs() -> SubstationParams:
    p = SubstationParams()

    print()
    print("  ╔══════════════════════════════════════════════╗")
    print("  ║   SUBSTATION LAYOUT GENERATOR  |  L&T        ║")
    print("  ╚══════════════════════════════════════════════╝")
    print()
    print("  Press Enter to accept the default shown in [brackets].")
    print("  All dimensions are in millimetres (mm).")

    # ── Power supply ──────────────────────────────────────────
    _section("POWER SUPPLY")
    p.supply_kv = _ask_int("Supply voltage (kV)", p.supply_kv)

    # ── Transformers ──────────────────────────────────────────
    _section("TRANSFORMERS")
    p.n_tx      = _ask_int("Number of transformers", p.n_tx)
    p.tx_rating = _ask_str("Rating per transformer (e.g. 1000 kVA)", p.tx_rating)
    print("    Transformer block size (per transformer):")
    p.tx_length = _ask_int("  TX LENGTH — horizontal (mm)", p.tx_length)
    p.tx_width  = _ask_int("  TX WIDTH  — vertical   (mm)", p.tx_width)

    # ── HT Panel ──────────────────────────────────────────────
    _section("HT PANEL")
    p.ht_incomers  = _ask_int("Number of incomers",  p.ht_incomers)
    p.ht_outgoings = _ask_int("Number of outgoings", p.ht_outgoings)
    p.ht_panel_length = _ask_int("HT Panel Length (mm)", p.ht_panel_length)
    p.ht_panel_width  = _ask_int("HT Panel Width (mm)",  p.ht_panel_width)

    # ── LT Panel ──────────────────────────────────────────────
    _section("LT PANEL")
    p.lt_incomers  = _ask_int("Number of incomers",  p.lt_incomers)
    p.lt_outgoings = _ask_int("Number of outgoings", p.lt_outgoings)
    p.lt_panel_length = _ask_int("LT Panel Length (mm)", p.lt_panel_length)
    p.lt_panel_width  = _ask_int("LT Panel Width (mm)",  p.lt_panel_width)

    # ── DG Synchronizer ───────────────────────────────────────
    _section("DG SYNCHRONIZER PANEL")
    print("    (Single synchronizer panel replaces individual DG sets in the layout)")
    print("    LENGTH = horizontal span on drawing  |  WIDTH = vertical depth on drawing")
    p.dg_sync_rating = _ask_str("Rating / label (e.g. 3×500 kVA)", p.dg_sync_rating)
    p.dg_sync_length = _ask_int("Panel LENGTH — horizontal (mm)", p.dg_sync_length)
    p.dg_sync_width  = _ask_int("Panel WIDTH  — vertical   (mm)", p.dg_sync_width)

    # ── Optional blocks ───────────────────────────────────────
    _section("OPTIONAL EQUIPMENT")
    p.has_apfc = _ask_bool("Include APFC Panel?", p.has_apfc)
    if p.has_apfc:
        print("    APFC panel size (one panel; repeated per transformer):")
        p.apfc_length = _ask_int("  APFC Panel LENGTH — horizontal (mm)", p.apfc_length)
        p.apfc_width  = _ask_int("  APFC Panel WIDTH  — vertical   (mm)", p.apfc_width)

    p.n_tx_ngr = _ask_int("Number of TX NGRs (0 = none, max 4)", p.n_tx_ngr)
    if p.n_tx_ngr > 4:
        p.n_tx_ngr = 4
        print("    ℹ  Capped at 4 TX NGRs.")
    if p.n_tx_ngr > 0:
        print("    TX NGR block size (same for each unit):")
        p.tx_ngr_length = _ask_int("  TX NGR LENGTH — horizontal (mm)", p.tx_ngr_length)
        p.tx_ngr_width  = _ask_int("  TX NGR WIDTH  — vertical   (mm)", p.tx_ngr_width)

    # ── Output file ───────────────────────────────────────────
    _section("OUTPUT")
    p.out_file = _ask_str("Output filename (.dxf)", p.out_file)
    if not p.out_file.endswith(".dxf"):
        p.out_file += ".dxf"

    # ── Summary ───────────────────────────────────────────────
    print()
    print("  ┌─ Layout summary ─────────────────────────────")
    print(f"  │  Supply         : {p.supply_kv} kV")
    print(f"  │  Transformers   : {p.n_tx} × {p.tx_rating}  ({p.tx_length}×{p.tx_width} mm)")
    print(f"  │  HT Panel       : {p.ht_incomers} incomer + {p.ht_outgoings} outgoings  ({p.ht_panel_length}×{p.ht_panel_width} mm)")
    print(f"  │  LT Panel       : {p.lt_incomers} incomer + {p.lt_outgoings} outgoings  ({p.lt_panel_length}×{p.lt_panel_width} mm)")
    print(f"  │  DG Synchronizer: {p.dg_sync_rating}  (L:{p.dg_sync_length} × W:{p.dg_sync_width} mm)")
    opts = []
    if p.has_apfc:    opts.append(f"APFC ({p.apfc_length}×{p.apfc_width} mm)")
    if p.n_tx_ngr > 0: opts.append(f"{p.n_tx_ngr}× TX NGR ({p.tx_ngr_length}×{p.tx_ngr_width} mm each)")
    print(f"  │  Optional       : {', '.join(opts) or 'none'}")
    print(f"  │  Output         : {p.out_file}")
    print("  └──────────────────────────────────────────────")
    input("\n  Press Enter to generate DXF…")

    return p