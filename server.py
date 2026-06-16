"""
server.py
Browser-based frontend server for the substation layout generator.
"""

import http.server
import json
import os
import webbrowser
from pathlib import Path

from inputs.schema import SubstationParams
from output.dxf_writer import write_dxf

BASE_DIR = Path(__file__).resolve().parent
HOST = "127.0.0.1"
PORT = 8000

class DXFRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.path = "/web/index.html"
        return super().do_GET()

    def end_headers(self):
        # Disable browser caching for all static files so edits are
        # always picked up immediately without a hard-refresh.
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_POST(self):
        if self.path != "/generate":
            self.send_error(404, "Not found")
            return

        content_length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(content_length)

        try:
            payload = json.loads(raw.decode("utf-8"))
        except ValueError:
            self._send_json({"error": "Invalid JSON payload."}, status=400)
            return

        try:
            params = self._params_from_payload(payload)
        except ValueError as exc:
            self._send_json({"error": str(exc)}, status=400)
            return

        try:
            out_path = write_dxf(params, output_dir=str(BASE_DIR))
        except Exception as exc:
            self._send_json({"error": f"DXF generation failed: {exc}"}, status=500)
            return

        self._send_json(
            {
                "success": True,
                "file": os.path.basename(out_path),
                "canvas_w": params.canvas_w,
                "canvas_h": params.canvas_h,
            }
        )

    def _send_json(self, data, status=200):
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _params_from_payload(self, payload):
        p = SubstationParams()

        p.supply_kv   = self._parse_positive_int(payload.get("supply_kv"),   "Supply voltage")
        p.n_tx        = self._parse_positive_int(payload.get("n_tx"),         "Number of transformers")
        p.tx_rating   = str(payload.get("tx_rating", "")).strip() or p.tx_rating
        p.tx_length   = self._parse_positive_int(payload.get("tx_length"),    "TX length")
        p.tx_width    = self._parse_positive_int(payload.get("tx_width"),     "TX width")

        p.ht_incomers     = self._parse_positive_int(payload.get("ht_incomers"),     "HT incomers")
        p.ht_outgoings    = self._parse_positive_int(payload.get("ht_outgoings"),    "HT outgoings")
        p.ht_panel_length = self._parse_positive_int(payload.get("ht_panel_length"), "HT panel length")
        p.ht_panel_width  = self._parse_positive_int(payload.get("ht_panel_width"),  "HT panel width")

        p.lt_incomers     = self._parse_positive_int(payload.get("lt_incomers"),     "LT incomers")
        p.lt_outgoings    = self._parse_positive_int(payload.get("lt_outgoings"),    "LT outgoings")
        p.lt_panel_length = self._parse_positive_int(payload.get("lt_panel_length"), "LT panel length")
        p.lt_panel_width  = self._parse_positive_int(payload.get("lt_panel_width"),  "LT panel width")

        p.dg_sync_count       = self._parse_positive_int(payload.get("dg_sync_count"),       "Number of DG units")
        p.dg_sync_unit_rating = self._parse_positive_int(payload.get("dg_sync_unit_rating"), "DG unit rating (kVA)")
        p.dg_sync_length      = self._parse_positive_int(payload.get("dg_sync_length"),      "DG sync length")
        p.dg_sync_width       = self._parse_positive_int(payload.get("dg_sync_width"),       "DG sync width")

        p.n_tx_ngr = self._parse_non_negative_int(payload.get("n_tx_ngr", 0), "Number of TX NGRs")
        if p.n_tx_ngr > 4:
            p.n_tx_ngr = 4

        p.has_apfc = bool(payload.get("has_apfc", False))

        if p.has_apfc:
            p.apfc_length = self._parse_positive_int(payload.get("apfc_length"), "APFC length")
            p.apfc_width  = self._parse_positive_int(payload.get("apfc_width"),  "APFC width")

        if p.n_tx_ngr > 0:
            p.tx_ngr_length = self._parse_positive_int(payload.get("tx_ngr_length"), "TX NGR length")
            p.tx_ngr_width  = self._parse_positive_int(payload.get("tx_ngr_width"),  "TX NGR width")

        out_file   = str(payload.get("out_file", "")).strip() or p.out_file
        p.out_file = os.path.basename(out_file)

        return p

    def _parse_positive_int(self, value, label):
        if value is None or value == "":
            raise ValueError(f"{label} is required.")
        try:
            parsed = int(value)
        except (TypeError, ValueError):
            raise ValueError(f"{label} must be a positive integer.")
        if parsed <= 0:
            raise ValueError(f"{label} must be greater than zero.")
        return parsed

    def _parse_non_negative_int(self, value, label):
        if value is None or value == "":
            return 0
        try:
            parsed = int(value)
        except (TypeError, ValueError):
            raise ValueError(f"{label} must be an integer (0 or more).")
        if parsed < 0:
            raise ValueError(f"{label} cannot be negative.")
        return parsed


def run_server():
    address = (HOST, PORT)
    print(f"Serving frontend at http://{HOST}:{PORT}/")
    print("Generating DXF files in the project directory.")
    webbrowser.open(f"http://{HOST}:{PORT}/")

    with http.server.ThreadingHTTPServer(address, DXFRequestHandler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")


if __name__ == "__main__":
    run_server()