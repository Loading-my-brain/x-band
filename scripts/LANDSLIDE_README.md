# Mingqi and Tom: landslide detection and potential road impacts

## Notebooks
- `Kaikoura_PostEvent_UNet_RF.ipynb`: standalone training and evaluation of U-Net and Random Forest using post-event Sentinel-2 and terrain predictors, with GNS Kaikoura V3 source/debris labels. Default settings are a pilot benchmark; rerunning does not necessarily recreate the later selected checkpoint.
- `Kaikoura_UNet_Road_Integration.ipynb`: frozen U-Net (epoch 77, threshold 0.31), RF (150 trees, threshold 0.28), road intersections and GNS reference comparison. U-Net weights and helper code are embedded. No retraining is required.
- `rf_150_trees.joblib.gz`: previously uploaded trained RF model, not training source code.

## Run in Google Colab
1. Open the desired notebook in Colab and run cells in order. Each notebook installs its Python dependencies. GPU is recommended for training.
2. Set `EE_PROJECT` to your own registered Earth Engine compute project and authenticate. Keep the GNS asset paths pointing to `projects/deep-voyage-479406-j9/assets/kaikoura_source_v3` and `kaikoura_debris_v3`.
3. For integration, the RF loader downloads the saved model from Google Drive. If downloading fails, upload the repository RF file to `/content/kaikoura_unet_roads/rf_150_trees.joblib.gz` and rerun the loader. Retain the notebook's model hash and library-version checks.
4. Roads are downloaded from the pinned team-repository revision. Outputs are generated in the notebook runtime and must be saved before that runtime expires.

## Interpretation
Inputs are post-event Sentinel-2 L1C reflectance and SRTM elevation/slope; this is not pre/post change detection. GNS polygons are mapped landslide reference labels, not verified road closures. Road-selected comparison tiles may overlap training/validation tiles, so their scores are reference agreement rather than independent test accuracy. Unknown coverage is not safe/open. Centreline intersections cannot establish remaining vehicle clearance or confirmed passability.

This module supplies potential impacts to downstream work; it is not the team's all-in-one routing notebook. Saved cell outputs and session metadata were removed for publication; model and analysis code were retained.

## Sources
- Sentinel-2: https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_HARMONIZED
- SRTM: https://developers.google.com/earth-engine/datasets/catalog/USGS_SRTMGL1_003
- GNS inventory: https://doi.org/10.17603/ds2-rpyg-0h84
- Roads: OpenStreetMap contributors, https://www.openstreetmap.org/copyright
