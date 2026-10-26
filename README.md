# x-band

GEOG 761 group project: assessing potential earthquake-related road impacts and vehicle access around Kaikōura. The workflow combines post-event Sentinel-2 landslide screening, lidar road-width estimates and vehicle-specific routing. The final integrated notebook uses a frozen Random Forest; U-Net remains a comparison model in the separate landslide notebooks.

## Start here

Open the [integrated workflow notebook](scripts/Kaikoura_Widths_Landslide_Routing_complete_version.ipynb) in Google Colab and follow the [integrated running instructions and provenance](scripts/INTEGRATED_WORKFLOW_README.md). Set an authorised Earth Engine compute project before running. The instructions identify dependencies, data access, model checksums and interpretation limits.

| Resource | Contents |
|---|---|
| [Integrated workflow](scripts/Kaikoura_Widths_Landslide_Routing_complete_version.ipynb) | Width estimation, frozen RF inference, road routing and off-road candidate connections |
| [U-Net / RF training](scripts/Kaikoura_PostEvent_UNet_RF.ipynb) | Spatial pilot benchmark, model training and validation experiments |
| [Landslide–road comparison](scripts/Kaikoura_UNet_Road_Integration.ipynb) | Frozen U-Net/RF predictions, road-centreline intersections and GNS reference comparison |
| [Landslide instructions](scripts/LANDSLIDE_README.md) | Component setup, dependencies and model-file guidance |
| [Width hand-off data](Data/) | OSM-way width outputs, metadata and routing interface |
| [Core road data](kaikoura_road_route/) | Supplied OSM road subset and geographic-context outline |
| [Recorded results](scripts/results_summary.json) | Verified numerical summary of saved runs, with evaluation scope |
| [Report figures](results/report_figures/) | Scientific figures, source metrics and offline plotting code |

## Scope and reproducibility

This is a retrospective research prototype, not an operational road-clearance service. Landslide overlap is not confirmed blockage; carriageway-width validation does not validate the separate drivable-width assumptions. Route costs include hand-set penalties, and roads missing assessment data remain unverified without an extra penalty. Off-road grid links require further inspection. See the integrated README for the full limitations.

The publication copies retain the existing team source and defaults. Outputs and session metadata were stripped from notebooks for readability; packaging did not rerun the models or generate new routing results. The recorded summary comes from saved outputs. Earth Engine authentication and external data services are required, and live OSM/data updates or unpinned packages can change later results.

## Attribution

X-Band contributors: Craig, Evan, Hinami, Mingqi, Neeravh and Tom. Module contributions and source provenance are documented in the notebook READMEs. Road data © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright), ODbL. The workflow also uses Sentinel-2, SRTM, GNS Kaikōura inventory V3, LINZ elevation data, NZTA road-width records, Hansen land masking and ESA WorldCover; retain the original data citations and applicable licences listed in the [integrated README](scripts/INTEGRATED_WORKFLOW_README.md).
