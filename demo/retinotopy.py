# %%
# %cd ../
# %config InlineBackend.figure_format='retina'

import altair as alt
import seaborn as sns
from IPython import get_ipython
from src.gabor_analysis.gabor_fit import GaborFit
from src.receptive_field.rf import ReceptiveField
from src.spikeloader import SpikeLoader
from src.utils.plots import gabor_interactive

get_ipython().run_line_magic("matplotlib", "inline")
get_ipython().run_line_magic("config", "InlineBackend.figure_format='retina'")
sns.set()

# %% tags=["parameters"]
# path_loader = "data/superstim_TX60_allsort.hdf5"
# path_rf = "data/superstim_TX60_allsort.hdf5"
# path_gabor = "data/superstim_TX60_allsort_gabor.hdf5"

# %%
# # Parameters
# path_npz = '/groups/stringer/home/josephs2/data/text32_500_TX59_2020_08_18.npz' 
# path_loader = '/groups/stringer/home/josephs2/data/text32_500_TX59_2020_08_18.hdf5' 
# path_rf = '/groups/stringer/home/josephs2/data/text32_500_TX59_2020_08_18.hdf5' 
# path_gabor = '/groups/stringer/home/josephs2/data/text32_500_TX59_2020_08_18.hdf5' 


# %%
f = SpikeLoader.from_hdf5(path_loader)
rf = ReceptiveField.from_hdf5(path_rf)
g = GaborFit.from_hdf5(path_gabor)

# %%
g.plot_params(f.pos)

# %% [markdown]
# ## Interactive Plot

# %%
alt.renderers.enable("mimetype")
gabor_interactive(f, g, n_samples=500)

# %%
