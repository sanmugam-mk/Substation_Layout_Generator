# Substation Equipment Layout Generator

## Overview

Substation Equipment Layout Generator is a Python-based engineering automation tool that generates AutoCAD DXF layouts for electrical substations.

The application automatically places:

* Transformers
* HT Panels
* LT Panels
* DG Synchronizer Panels
* APFC Panels
* DG NGR
* TX NGR
* Ancillary Rooms
* Rolling Shutters
* Main Entrance

based on user inputs and engineering spacing rules.

The generated output can be opened directly in:

* AutoCAD
* BricsCAD
* LibreCAD

---

## Features

### Automatic Layout Generation

Generates equipment layouts automatically based on:

* Supply Voltage
* Number of Transformers
* Transformer Rating
* HT Panel Configuration
* LT Panel Configuration
* DG Configuration
* Ancillary Room Requirements

### DXF Export

Creates production-ready DXF drawings.

### Web Interface

Provides a browser-based interface for entering project parameters and generating layouts.

### Engineering Rule Compliance

Implements:

* Equipment clearances
* Transformer spacing
* HT/LT panel positioning
* DG equipment spacing
* Ancillary room placement

---

## Technology Stack

### Backend

* Python
* Flask
* ezdxf

### Frontend

* HTML
* CSS
* JavaScript

### CAD Generation

* DXF (AutoCAD compatible)

---

## Project Structure

```text
substation_mod/
│
├── core/
├── engine/
├── inputs/
├── output/
├── output_layout/
├── web/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── main.py
├── server.py
└── README.md
```

---

## Running Locally

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start Server

```bash
python server.py
```

### Open Browser

```text
http://localhost:5000
```

---

## Generated Layout

Typical generated layout includes:

```text
UPS / SCADA / Maintenance / Toilet

TX1  TX2  TX3  HT Panel Room

Main LT Panel

DG Synchronizer
APFC Panels
DG NGR
TX NGR
```

with automatic room sizing and equipment placement.

---

## Done by 

Sanmugam

Electrical Engineering Automation Project

Developed for automated substation equipment layout generation and DXF drafting.
