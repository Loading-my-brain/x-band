# Kaikōura scientific figures

Three report-ready figures for the X-Band project. This folder contains figures,
small plotting inputs and offline plotting code, not an individual report.

| Figure | Files | What is shown |
| --- | --- | --- |
| 1 | `figure1_pipeline.*` | The implemented landslide, road-width and routing pipeline, including the optional off-road branch. |
| 2 | `figure2_assessment.*` | Frozen U-Net/RF reference agreement and NZTA carriageway-width validation. |
| 3 | `Figure3_integrated_route.*` | Actual saved Culverden–Kaikōura route geometry, with an enlarged final approach and graph-edge assessment status. |

Each figure is supplied as 300 dpi PNG and vector PDF/SVG, at a print width of
6.9 inches. The archived originals are kept in this directory. Reproduction writes
to a separate directory by default, so it does not overwrite them.

## Reproduce offline

Install the plotting dependencies once, then run from this directory:

```sh
python -m pip install -r requirements.txt
python reproduce.py
```

The figures will appear in `reproduced/`. A different destination can be selected:

```sh
python reproduce.py --out-dir /path/to/output
```

No Google account, Earth Engine access, model downloads or network basemap is
needed. The scripts only read the bundled JSON/GeoJSON. They do not rerun training,
inference, width estimation or routing. Dependencies must already be installed
for a fully offline run. The pinned versions are the tested plotting environment;
other versions can produce small rendering differences.

For an offline verification run with Python network connections blocked:

```sh
python verify_reproduction.py
```

This recreates all nine outputs and compares PNG pixel arrays with the archived
figures. PDF/SVG timestamps and internal identifiers may differ even when their
appearance matches. Offline verification on 26 October 2026 reproduced all three
archived PNGs pixel for pixel and created all nine PNG/PDF/SVG outputs.
`SHA256SUMS` records the exact published package files.

## Sources and interpretation

**Figure 1:** The diagram is drawn from the saved integrated notebook. The final
integration uses the frozen Random Forest; U-Net is a separate comparison model.
Width and landslide assessments join to the routing graph by OSM way ID. Routes
outside the assessment coverage remain unverified and receive no extra penalty.
The off-road branch has no measured vehicle-clearance validation.

**Figure 2a:** Values are from the saved 15 October 2026 road-comparison outputs.
The 1,393,305 shared valid pixels are in road-selected tiles, which may overlap
training or validation. Scores therefore describe agreement with the GNS mapped
landslide inventory, not a new independent test and not confirmed blockage
accuracy. A larger predicted overlap is not proof of a better blockage detector.

**Figure 2b:** Values are taken from `handoff_metadata.json` in the width handoff.
The slope-only and calibrated estimates have different usable validation samples
(36 and 41 records). This is not a paired before/after comparison. The calibration
assessment concerns carriageway width, not the more lenient drivable-width rule
or field-confirmed vehicle passability. Metadata retain three decimal places;
the saved notebook displays fewer. The minimal plotted records are in
`assessment_metrics.json`.

**Figure 3:** Geometry and status were extracted from the saved Folium map in
`Kaikoura_Widths_Landslide_Routing_complete_version.html`, cell 74 (one-based),
execution counter `In[46]`. The supplied baseline is the fastest route ignoring
checks. Both vehicles have identical selected geometries and statuses in that
export; the plotting script verifies this. Coordinates are supplied in WGS84 and
projected to NZTM2000 / EPSG:2193 for the map.

The colours describe saved **graph-edge classifications**, not exact spatial
measurement coverage or confirmed road safety. Assessments of clipped OSM ways
can be attached to longer graph edges. The selected route's reported 87.2 minutes
combines modelled driving time with artificial unknown-condition penalties and
is not a validated arrival-time prediction. Most of the route is unverified.

These integrated runs are distinct from the earlier routing brief's experiments
with 400 m circular stand-in closures, 3.7× travel-time calibration and helicopter
comparisons. Those earlier scenario results are not included in these figures.

More source details are recorded in `provenance.json`. The team code is at
[Loading-my-brain/x-band](https://github.com/Loading-my-brain/x-band).

## Attribution

Road geometry is derived from OpenStreetMap: © OpenStreetMap contributors,
[copyright and ODbL information](https://www.openstreetmap.org/copyright).
GNS Kaikōura V3 landslide reference:
[DesignSafe dataset DOI](https://doi.org/10.17603/ds2-rpyg-0h84).
The width validation uses Waka Kotahi NZTA National Road Centreline–RCA data.
Credit the X-Band team for the underlying saved model, width and routing outputs.
No licence is asserted here over third-party source data beyond their own terms.
