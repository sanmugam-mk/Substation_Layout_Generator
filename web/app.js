// ── Element refs ──────────────────────────────────────────
const form           = document.getElementById("layout-form");
const genBtn         = document.getElementById("generate-btn");
const statusIcon     = document.getElementById("status-icon");
const statusText     = document.getElementById("status");
const resultPanel    = document.getElementById("result");
const downloadLink   = document.getElementById("download-link");
const resultFilename = document.getElementById("result-filename");
const dimensionsText = document.getElementById("dimensions");

const apfcToggle = form.elements["has_apfc"];
const nTxNgr     = form.elements["n_tx_ngr"];
const apfcFields = document.getElementById("apfc-fields");
const ngrFields  = document.getElementById("ngr-fields");

// ── Optional equipment toggle ─────────────────────────────
function syncOptional() {
  const apfcOn = apfcToggle.checked;
  const ngrOn  = parseInt(nTxNgr.value || "0") > 0;

  apfcFields.classList.toggle("disabled", !apfcOn);
  ngrFields .classList.toggle("disabled",  !ngrOn);
  apfcFields.querySelectorAll("input").forEach(i => { i.disabled = !apfcOn; });
  ngrFields .querySelectorAll("input").forEach(i => { i.disabled = !ngrOn; });
}

apfcToggle.addEventListener("change", syncOptional);
nTxNgr    .addEventListener("input",  syncOptional);
syncOptional();

// ── Live summary sidebar ──────────────────────────────────
const summaryFields = {
  "s-supply": () => (form.elements["supply_kv"].value || "—") + " kV",
  "s-tx": () => {
    const n = form.elements["n_tx"].value || "—";
    const r = form.elements["tx_rating"].value || "—";
    return `${n} × ${r}`;
  },
  "s-ht": () => {
    const l = form.elements["ht_panel_length"].value || "—";
    const w = form.elements["ht_panel_width"].value  || "—";
    return `${l} × ${w} mm`;
  },
  "s-lt": () => {
    const l = form.elements["lt_panel_length"].value || "—";
    const w = form.elements["lt_panel_width"].value  || "—";
    return `${l} × ${w} mm`;
  },
  "s-dg": () => {
    const c = form.elements["dg_sync_count"].value || "—";
    const r = form.elements["dg_sync_unit_rating"].value || "—";
    const l = form.elements["dg_sync_length"].value || "—";
    const w = form.elements["dg_sync_width"].value  || "—";
    return `${c}×${r} kVA  (${l} × ${w} mm)`;
  },
  "s-opt": () => {
    const opts = [];
    if (apfcToggle.checked) opts.push("APFC");
    const n = parseInt(nTxNgr.value || "0");
    if (n > 0) opts.push(`${n}× TX NGR`);
    return opts.length ? opts.join(", ") : "None";
  },
  "s-file": () => form.elements["out_file"].value || "—",
};

function updateSummary() {
  for (const [id, fn] of Object.entries(summaryFields)) {
    const el = document.getElementById(id);
    if (el) el.textContent = fn();
  }
}

form.addEventListener("input",  updateSummary);
form.addEventListener("change", updateSummary);
updateSummary();

// ── Status helpers ────────────────────────────────────────
function setStatus(text, state = "idle") {
  statusText.textContent = text;
  statusIcon.className   = "status-icon " + (state !== "idle" ? state : "");
  statusText.className   = "status-text"  + (state === "err" ? " err" : "");
}

// ── Form data ─────────────────────────────────────────────
function collectFormData() {
  return {
    supply_kv:           form.elements["supply_kv"].value,
    n_tx:                form.elements["n_tx"].value,
    tx_rating:           form.elements["tx_rating"].value,
    tx_length:           form.elements["tx_length"].value,
    tx_width:            form.elements["tx_width"].value,
    ht_incomers:         form.elements["ht_incomers"].value,
    ht_outgoings:        form.elements["ht_outgoings"].value,
    ht_panel_length:     form.elements["ht_panel_length"].value,
    ht_panel_width:      form.elements["ht_panel_width"].value,
    lt_incomers:         form.elements["lt_incomers"].value,
    lt_outgoings:        form.elements["lt_outgoings"].value,
    lt_panel_length:     form.elements["lt_panel_length"].value,
    lt_panel_width:      form.elements["lt_panel_width"].value,
    dg_sync_count:       form.elements["dg_sync_count"].value,
    dg_sync_unit_rating: form.elements["dg_sync_unit_rating"].value,
    dg_sync_length:      form.elements["dg_sync_length"].value,
    dg_sync_width:       form.elements["dg_sync_width"].value,
    has_apfc:            apfcToggle.checked,
    n_tx_ngr:            form.elements["n_tx_ngr"].value,
    apfc_length:         form.elements["apfc_length"].value,
    apfc_width:          form.elements["apfc_width"].value,
    tx_ngr_length:       form.elements["tx_ngr_length"].value,
    tx_ngr_width:        form.elements["tx_ngr_width"].value,
    out_file:            form.elements["out_file"].value,
  };
}

// ── Submit ────────────────────────────────────────────────
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  resultPanel.classList.add("hidden");
  setStatus("Generating DXF…", "busy");
  genBtn.disabled = true;

  try {
    const res  = await fetch("/generate", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify(collectFormData()),
    });

    const data = await res.json();

    if (!res.ok || data.error) {
      setStatus(data.error || "Generation failed.", "err");
      return;
    }

    const filename = data.file || form.elements["out_file"].value;
    downloadLink.href          = "/" + encodeURIComponent(data.file);
    downloadLink.download      = filename;
    resultFilename.textContent = filename;
    dimensionsText.textContent = `Canvas: ${data.canvas_w} × ${data.canvas_h} mm`;
    resultPanel.classList.remove("hidden");
    setStatus("DXF generated.", "ok");

  } catch (err) {
    setStatus("Cannot reach the server.", "err");
  } finally {
    genBtn.disabled = false;
  }
});