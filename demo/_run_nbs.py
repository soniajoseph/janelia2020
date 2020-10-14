import logging
from pathlib import Path

import nbconvert
import jupytext
import papermill as pm
import os

"""Execute parameterized notebooks.

1. Convert py to ipynb with nbconvert and set kernelspec.
2. Run said notebook with papermill.
3. Delete said notebook.

"""

# +
# name, date = 'TX56', '2020_08_04'
data_path =  '/groups/stringer/home/josephs2/data/text32_500_TX59_2020_08_18_coding_neurons.npz'
hdf5_path = os.path.splitext(data_path)[0] + '.hdf5'
# hdf5_path = '/groups/stringer/home/josephs2/data/text32_500_TX59_2020_08_18.hdf5' 

nbs = ["preprocess", "run_rf", "retinotopy", "cca_stimuli"]
# nbs = ["retinotopy", "cca_stimuli"]

path_output = Path("outputs/")

import os
from os import path

# -

parameters = dict(
    path_npz=Path(data_path).with_suffix(".npz").as_posix(),
#     path_img="/groups/pachitariu/pachitariulab/data/STIM/text32_500.mat",
    path_loader=hdf5_path,
    path_rf=hdf5_path,
    path_gabor=hdf5_path,
)

path_output.mkdir(parents=True, exist_ok=True)

for nb in nbs:
    try:
        ntb = jupytext.read(nb + ".py")
        ntb.metadata["kernelspec"] = {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        }
        jupytext.write(ntb, nb + ".ipynb")
        
        print(nb)
        pm.execute_notebook(
            f"{nb}.ipynb",
            output_path=(path_output / f"{nb}_output.ipynb").as_posix(),
            parameters=parameters,
        )
        
        
    except pm.exceptions.PapermillExecutionError as e:
        logging.error(f"Error at {nb}.")
        raise e
    finally:
        Path(nb + ".ipynb").unlink(missing_ok=True)




