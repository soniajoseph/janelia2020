import logging
from pathlib import Path

import nbconvert
import jupytext
import papermill as pm
import os
from os import path

"""Execute parameterized notebooks.

1. Convert py to ipynb with nbconvert and set kernelspec.
2. Run said notebook with papermill.
3. Delete said notebook.

"""

# +
# root
data_root = '/groups/pachitariu/pachitariulab/datasets/v1RF'

os.path.isdir(data_root)
# stimulus path
path_img = "/groups/pachitariu/pachitariulab/data/STIM/text32_500.mat"

# loop over experiments
dbs = [
#     {'mouse_name': 'TX57', 'date': '2020_08_18'},
#        {'mouse_name': 'TX58', 'date': '2020_08_14'},
#        {'mouse_name': 'TX59', 'date': '2020_08_05'}, # has error in istim. check nb.
       {'mouse_name': 'TX59', 'date': '2020_08_18'},
       {'mouse_name': 'TX60', 'date': '2020_08_14'}
      ]

for db in dbs:
    file_name = 'text32_500_%s_%s.npz'%(db['mouse_name'], db['date'])
    data_path = os.path.join(data_root, 
                        file_name)
    print("Reading from ", data_path)
    hdf5_path = '/groups/stringer/home/josephs2/data/' + os.path.splitext(file_name)[0] + '.hdf5'
    print("Saving at ", hdf5_path)

    nbs = ["preprocess", "run_rf", "run_gabor", "retinotopy", "cca_stimuli"]
#     nbs = ['run_gabor']

    path_output = Path("outputs/" + 'text32_500_%s_%s_'%(db['mouse_name'], db['date']))
    
    parameters = dict(
        path_npz=Path(data_path).with_suffix(".npz").as_posix(),
        path_hdf5=hdf5_path,
        path_img=path_img,
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
            continue
        finally:
            Path(nb + ".ipynb").unlink(missing_ok=True)


# -




