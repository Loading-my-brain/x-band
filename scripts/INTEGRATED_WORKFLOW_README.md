# X-Band integrated Kaikōura workflow

`scripts/Kaikoura_Widths_Landslide_Routing_complete_version.ipynb` is the team's integrated road-width, landslide-screening, road-routing and off-road-candidate notebook. Its landslide stage uses the saved **150-tree Random Forest at threshold 0.28**. U-Net is retained in the separate comparison notebooks, not used in this integrated routing run.

## Run in Google Colab

1. Open `scripts/Kaikoura_Widths_Landslide_Routing_complete_version.ipynb` in Colab. Run the setup cell, then the notebook cells in order. The workflow uses `/content` paths and Colab download/authentication helpers; a CPU runtime can perform the frozen RF inference. No model training is performed here.
2. In **Project inputs**, replace the retained `EE_PROJECT = 'geo-761'` with an Earth Engine-enabled Google Cloud project your authenticated account is authorised to use. Complete the interactive Earth Engine sign-in. Never put credentials or tokens into the notebook.
3. Retain the GNS asset paths unless using an explicitly documented alternative copy:
   - `projects/deep-voyage-479406-j9/assets/kaikoura_source_v3`
   - `projects/deep-voyage-479406-j9/assets/kaikoura_debris_v3`
   The authenticated account needs read access to both. These are mapped source/debris polygons, not road-closure labels.
4. The RF loader downloads the model from `https://raw.githubusercontent.com/NMC31/random_forest_761/master/rf_150_trees.joblib`. The audited `master` revision was `15626c009bf45ffde7cf1b785c1b7f540432e465`; its default `main` branch was empty. The notebook verifies model hashes, feature count, tree count, library version and saved prediction parity. If downloading fails, upload the repository's `scripts/rf_150_trees.joblib.gz` to `/content` or `/content/kaikoura_unet_roads/`, then rerun the loader. The loader accepts either the verified compressed or extracted model. Keep all checks enabled.
5. Width processing creates `/content/xband_roads/handoff/by_osm_id.csv`. RF processing creates `/content/kaikoura_unet_roads/outputs/landslide_by_osm_id_rf.csv`. The hand-off cell copies these and downloads the AOI shapefile into the working directory before routing. Keep the original defaults for reproducing the documented scenarios. Route endpoints, vehicle widths, clearance and penalty settings are explicit inputs.
6. Save the generated tables, figures, geographic outputs and an executed notebook before ending the Colab session. Data services and OSM queries are live; a later run may differ as source data or unpinned packages change. The final off-road section is enabled by its own `RUN_OFFROAD` setting.

### Dependencies

The setup cell installs `geopandas`, `rasterio`, `shapely`, `pyproj`, `requests`, `matplotlib`, `earthengine-api`, `folium`, **`scikit-learn==1.6.1`**, and `osmnx`. Other direct imports include `numpy`, `pandas`, `scipy`, `networkx`, `pyogrio`, `joblib`, `branca`, `IPython` and `google.colab`; Colab or the installed packages supply these. Routing documents `osmnx>=2.0` and `geopandas>=1.0`. Only scikit-learn is exactly pinned, so this is not a fully frozen environment. If Colab already imported a different scikit-learn version, restart the runtime after installation and rerun from the top. No external Python source is fetched for the embedded landslide helpers.

### Model and road checksums

- Compressed RF SHA-256: `db43c611a13967c447049e6934e617a4b4111cfaf9fc8fc8671c6e0c2cd1f5ad`.
- Extracted RF SHA-256: `f19a1d236938093a6b905aedf80cb8893c362e356ec9495de8eef3b73c8baad6`.
- Core road data: `kaikoura_road_route/kai_route.gpkg`, pinned repository revision `8d739079424b3b6c7077f470346a8840f20a0e1c`, SHA-256 `127841d08d83cfc7a3ec82cf34f850d92d6d66550e650cea4304a2a1aff26b0e`.

## Provenance and recorded results

This publication copy was prepared on **26 October 2026** from the original team notebook shared on 25 October 2026. Original source: [team notebook](https://colab.research.google.com/drive/1eAPxteeJUILxwFaYvdQ6KTG5ZoY4UNsy).

The original notebook contains 84 cells, including 52 code cells. All source text, code defaults and cell order were retained exactly. Outputs, execution counters and Colab/session metadata were removed; neutral cell IDs were added for notebook-format compatibility. All 52 code-cell sources also match the executed HTML export after ignoring terminal newline differences introduced by HTML rendering. No inference, training or route calculation was rerun for publication.

- Original notebook filename: `Kaikoura_Widths_Landslide_Routing_complete_version.ipynb`.
- Original downloaded notebook SHA-256: `b6b17ca822ceca86ad681acedd354fba609206f785ab6ea72fdfb0c6e808dd56`.
- Executed HTML filename: `Kaikoura_Widths_Landslide_Routing_complete_version.html`.
- Executed HTML SHA-256: `e50c07017ef354b4f289d56b4f662fc8e3e40795ba5d222c09fd8250856a2f5e`.
- Published stripped notebook SHA-256: `6ab2bced2017f2fbb85c17770e9913e9b8b2c143dabe0deea3f39f376b195df3`.

`scripts/results_summary.json` transcribes verified numerical results from those saved outputs and identified component metrics. It records provenance and evaluation scope; it is not a new execution or a substitute for the original outputs.

## Interpretation and limitations

- RF/GNS scores describe agreement on road-selected pixels that overlap development areas, not an independent test or road-closure accuracy. The 10 m satellite grid cannot establish remaining vehicle clearance. This is post-event classification, not pre/post change detection.
- NZTA validation tests the stricter **carriageway-width** rule. The more permissive **drivable-width** rule and 1 m clearance margin remain assumptions. NZTA records may describe rebuilt roads; lidar and land-cover dates differ from the earthquake.
- Predicted continuous landslide overlap defaults to **unknown**, not confirmed closure. Width `no`/`unknown` classifications and hand-set landslide penalties affect the route objective. Roads absent from assessment files remain **unverified without an added penalty**. A route labelled clear does not establish safety.
- Local and Culverden road-only scenarios contain approximately 67% and 84% unverified distance, respectively. Reported costs combine driving estimates and preferences, not validated convoy arrival times. A*–Dijkstra consistency checks verify the defined search objective, not real-world passability. No saved RF-on/off ablation isolates the landslide layer's benefit.
- Off-road links are candidate grid connections. They lack width/soil-strength validation, can include existing road cells, and use a 20 m grid with temporal/coverage limitations. The final extension does not implement the earlier routing brief's bridge-weight, fording-depth or damaged-road speed adjustments. That brief's simulated circular landslides are a separate experiment.

## Data and team attribution

This integrated notebook combines work by the X-Band team: Hinami and Evan (road widths), Mingqi and Tom (landslide modelling and road impacts), and Craig and Neeravh (routing), with team integration and extensions. Cite the group repository and the relevant original data sources; the publication packaging does not change code authorship.

- [Sentinel-2 L1C TOA](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_HARMONIZED), [SRTM elevation](https://developers.google.com/earth-engine/datasets/catalog/USGS_SRTMGL1_003), and [Hansen v1.10 land mask](https://developers.google.com/earth-engine/datasets/catalog/UMD_hansen_global_forest_change_2022_v1_10).
- [GNS Kaikōura landslide inventory V3](https://doi.org/10.17603/ds2-rpyg-0h84).
- [LINZ Kaikōura 2016–2017 1 m DEM](https://nz-elevation.s3.ap-southeast-2.amazonaws.com/canterbury/kaikoura_2016-2017/dem_1m/2193/collection.json), [national 1 m DEM](https://nz-elevation.s3.ap-southeast-2.amazonaws.com/new-zealand/new-zealand/dem_1m/2193/collection.json), and [national contour-derived 8 m DEM](https://nz-elevation.s3.ap-southeast-2.amazonaws.com/new-zealand/new-zealand-contour/dem_8m/2193/collection.json).
- [NZTA National Road Centreline RCA data](https://opendata-nzta.opendata.arcgis.com/datasets/NZTA::national-road-centreline-road-controlling-authority-data), CC BY 4.0.
- Road data © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright), ODbL. The core road snapshot date is unverified; the supplied district outline provides context.
- [ESA WorldCover 2021 v200](https://doi.org/10.5281/zenodo.7254221), used by the off-road extension.
