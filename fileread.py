import pandas as pd
import os


def load_trajectories(data_dir="Data/"):

    id_counter = 0
    trajectories = {}

    # Loop over all data subdirectories
    for subdir, dirs, files in os.walk(data_dir):

        # Loop over all plt files
        for file in files:
            if not file.endswith(".plt"):
                continue

            # Convert plt files to Panda frames
            df = pd.read_csv(os.path.join(subdir, file), sep=',', 
                             skiprows=[0,1,2,3,4,5], usecols=[0,1,6],
                             names=["Longitude", "Latitude", "Time"], header=None)

            # Attach trahejectories to user
            trajectories[id_counter] = df
            id_counter += 1

    return trajectories
            

trajectories = load_trajectories()

# Get trajectories of first user
#trajectories[0]

from IPython import embed; embed()