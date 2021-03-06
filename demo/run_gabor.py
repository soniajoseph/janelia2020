# -*- coding: utf-8 -*-
# %%
# %cd ../
# %config InlineBackend.figure_format='retina'

import logging

import numpy as np
import seaborn as sns
from src.gabor_analysis.gabor_fit import GaborFit
from src.receptive_field.rf import ReceptiveField
from pathlib import Path

logging.getLogger().setLevel(logging.INFO)
sns.set()

# %% tags=["parameters"]
path_loader = "/groups/stringer/home/josephs2/data/text32_500_TX59_2020_08_18.hdf5"
path_rf = "/groups/stringer/home/josephs2/data/text32_500_TX59_2020_08_18.hdf5"
path_rf_pcaed = "/groups/stringer/home/josephs2/data/text32_500_TX59_2020_08_18rf_pcaed.npy"

# %%
path_loader = Path(path_loader)
path_rf_pcaed = path_loader.parent / (path_loader.stem + "rf_pcaed.npy")

# %%
rf_pcaed = np.load(path_rf_pcaed)
rf = ReceptiveField.from_hdf5(path_rf)


def penalties():
    out = np.zeros((5, 2), dtype=np.float32)
    out[GaborFit.KEY["σ"]] = (0.04, 2.0)
    out[GaborFit.KEY["λ"]] = (0.6, 0.85)
    out[GaborFit.KEY["γ"]] = (0.8, 0.5)
    return out


g = GaborFit(
    n_pc=0,
    optimizer={"name": "adam", "step_size": 2e-2},
    params_init={"σ": 2, "θ": 0.0, "λ": 1.0, "γ": 1.5, "φ": 0.0, "pos_x": 0.0, "pos_y": 0.0},
    penalties=penalties(),
).fit(rf_pcaed)
g.plot()
g.save_append(path_loader, overwrite_group=True)

# %% [markdown]
"""
### Diagnostic

As a diagnostic, we check compare
- the correlations between the PCAed RFs and raw RFs and 
- the correlations between the fitted Gabor RFs and raw RFs.

If out Gabor fit can cover enough "receptive field space", there should be a linear correspondence between these two models.
"""

# %%
g.plot_corr(rf.rf_, rf_pcaed)
