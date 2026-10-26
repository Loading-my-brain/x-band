"""Replot with Python networking blocked and compare archived PNG pixels."""
from pathlib import Path
import hashlib
import json
import os
import runpy
import socket
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
os.environ.update(PROJ_NETWORK='OFF', MPLBACKEND='Agg')

def no_network(*args, **kwargs):
    raise RuntimeError('Network access is disabled during offline figure verification.')

socket.create_connection = no_network
socket.socket.connect = no_network
socket.socket.connect_ex = no_network

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

records = []
with tempfile.TemporaryDirectory(prefix='xband-figures-') as temp:
    dest = Path(temp)
    for script in ['plot_pipeline.py', 'plot_assessment.py', 'plot_route.py']:
        plt.rcdefaults()  # Match the fresh process used by reproduce.py.
        sys.argv = [script, '--out-dir', str(dest)]
        runpy.run_path(str(ROOT/script), run_name='__main__')
        plt.close('all')
    for stem in ['figure1_pipeline', 'figure2_assessment', 'Figure3_integrated_route']:
        old = np.array(Image.open(ROOT/f'{stem}.png').convert('RGBA'))
        new = np.array(Image.open(dest/f'{stem}.png').convert('RGBA'))
        match = old.shape == new.shape and np.array_equal(old, new)
        for ext in ['png', 'pdf', 'svg']:
            assert (dest/f'{stem}.{ext}').stat().st_size > 0
        records.append({'figure':stem, 'png_pixels_identical':bool(match),
                        'size_pixels':[int(old.shape[1]),int(old.shape[0])]})
        assert match, f'{stem}: rendering differs from the archived PNG; check dependency versions.'
print(json.dumps({'offline_reproduction':'passed', 'figures':records}, indent=2))
