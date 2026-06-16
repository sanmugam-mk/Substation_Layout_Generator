from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
import os

from inputs.schema import SubstationParams
from output.dxf_writer import write_dxf

app = Flask(__name__,
            static_folder="web",
            static_url_path="/web")

BASE_DIR = Path(__file__).resolve().parent


@app.route("/")
def home():
    return send_from_directory("web", "index.html")


@app.route("/generate", methods=["POST"])
def generate():

    payload = request.get_json()

    try:
        params = params_from_payload(payload)

        out_path = write_dxf(
            params,
            output_dir=str(BASE_DIR / "output_layout")
        )

        return jsonify({
            "success": True,
            "file": os.path.basename(out_path),
            "canvas_w": params.canvas_w,
            "canvas_h": params.canvas_h,
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


def params_from_payload(payload):

    p = SubstationParams()

    p.supply_kv = int(payload["supply_kv"])

    p.n_tx = int(payload["n_tx"])
    p.tx_rating = payload["tx_rating"]
    p.tx_length = int(payload["tx_length"])
    p.tx_width = int(payload["tx_width"])

    p.ht_incomers = int(payload["ht_incomers"])
    p.ht_outgoings = int(payload["ht_outgoings"])
    p.ht_panel_length = int(payload["ht_panel_length"])
    p.ht_panel_width = int(payload["ht_panel_width"])

    p.lt_incomers = int(payload["lt_incomers"])
    p.lt_outgoings = int(payload["lt_outgoings"])
    p.lt_panel_length = int(payload["lt_panel_length"])
    p.lt_panel_width = int(payload["lt_panel_width"])

    p.dg_sync_count = int(payload["dg_sync_count"])
    p.dg_sync_unit_rating = int(payload["dg_sync_unit_rating"])
    p.dg_sync_length = int(payload["dg_sync_length"])
    p.dg_sync_width = int(payload["dg_sync_width"])

    p.n_tx_ngr = int(payload.get("n_tx_ngr", 0))
    p.has_apfc = bool(payload.get("has_apfc", False))

    if p.has_apfc:
        p.apfc_length = int(payload["apfc_length"])
        p.apfc_width = int(payload["apfc_width"])

    if p.n_tx_ngr > 0:
        p.tx_ngr_length = int(payload["tx_ngr_length"])
        p.tx_ngr_width = int(payload["tx_ngr_width"])

    p.out_file = payload.get(
        "out_file",
        "substation_layout.dxf"
    )

    return p


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)