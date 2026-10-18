# X-Band road widths - handoff to routing

Join layer `by_osm_id` to the routing graph on **osm_id = edge attribute osmid** (function `attach_road_widths` in the notebook).

| Column | Meaning |
|---|---|
| osm_id / full_id | OSM way id as a number / with the 'w' prefix |
| width_median_m | typical carriageway width (calibrated against NZTA) |
| drive_pinch_m | narrowest drivable width holding across two neighbouring cross-sections - use for "does it fit?" |
| share_measured / drive_share | fraction of the road's 50 m cross-sections with a usable carriageway / drivable width |
| n_flagged | cross-sections that looked narrow or had nothing flat at the centre (possible debris) |
| passable_<vehicle> | yes / no / unknown (vehicle width + 1.0 m clearance) |
| reason_<vehicle> | why it is no / unknown |

'unknown' must never be treated as 'yes'. Settings, accuracy, sources and limitations: handoff_metadata.json.
