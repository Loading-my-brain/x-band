"""Recreate the three figures from bundled assets; no network data is used."""
from pathlib import Path
import argparse
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--out-dir', type=Path, default=ROOT / 'reproduced')
args = parser.parse_args()
destination = args.out_dir.resolve()
destination.mkdir(parents=True, exist_ok=True)
environment = dict(os.environ, PROJ_NETWORK='OFF', MPLBACKEND='Agg')
for script in ['plot_pipeline.py', 'plot_assessment.py', 'plot_route.py']:
    subprocess.run([sys.executable, str(ROOT/script), '--out-dir', str(destination)],
                   check=True, env=environment)
print('All three figures reproduced:', destination)
