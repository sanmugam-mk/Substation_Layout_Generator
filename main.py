"""
Substation Layout Generator — L&T
==================================
Entry point. Run this file.

    python main.py

Project structure:
    main.py              ← you are here
    inputs/
        form.py          ← interactive terminal form (all user prompts)
        schema.py        ← SubstationParams dataclass
    engine/
        layout.py        ← geometry calculator (sizes, positions)
        placer.py        ← equipment placement logic
    core/
        constants.py     ← all magic numbers in one place
        layers.py        ← DXF layer definitions
        primitives.py    ← low-level draw helpers (rect, text, dim…)
    output/
        dxf_writer.py    ← assembles the final DXF document
"""

import sys

from inputs.form import collect_inputs
from output.dxf_writer import write_dxf
from server import run_server


def run_cli():
    params = collect_inputs()
    out_path = write_dxf(params)
    print(f"\n  ✓  DXF saved → {out_path}")
    print(f"  Canvas : {params.canvas_w} × {params.canvas_h} mm")
    print(f"  Supply : {params.supply_kv} kV\n")


def main():
    if len(sys.argv) > 1 and sys.argv[1].lower() in ("--cli", "cli"):
        run_cli()
    else:
        run_server()


if __name__ == "__main__":
    main()
