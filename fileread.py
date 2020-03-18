import pandas as pd
import os
import math
import numpy as np


def load_trajectories(data_dir="Data/"):

    id_counter = 0
    trajectories = {}

    user_map_file = open("user_id_mapping.csv", "w")

    # Loop over all data subdirectories
    for subdir, dirs, files in os.walk(data_dir):

        # Loop over all plt files
        for file in files:
            if not file.endswith(".plt"):
                continue

            user_map_file.write(f"{file}, {id_counter}\n")


            # Convert plt files to Panda frames
            df = pd.read_csv(os.path.join(subdir, file), sep=',', 
                             skiprows=[0,1,2,3,4,5], usecols=[0,1,6],
                             names=["Longitude", "Latitude", "Time"], header=None)

            # Attach trahejectories to user
            trajectories[id_counter] = df
            id_counter += 1

    return trajectories
            

def convert_to_fixed_timesteps(trajectories, timestep_size=60):
    """ Replaces the time column and  """

    def time_to_timestep(row):
        h, m, s = map(int, row["Time"].split(':'))
        timestep = round((h*3600+m*60+s)/timestep_size)
        return timestep

    for i, t in trajectories.items():
        t["Timestep"] = t.apply(time_to_timestep, axis=1)
        t = t.drop_duplicates("Timestep")
        t = t.set_index("Timestep")
        trajectories[i] = t
        
    return trajectories


def save_numpy_matrix(trajectories, filename="matrix.npy"):
    # Allocate matrix
    timesteps = math.ceil(24*60*60/timestep_size) + 1
    traces = len(trajectories.keys())
    table = np.zeros((timesteps, traces, 2))

    for user_id, df in trajectories.items():
        for timestep, row in df.iterrows():
            table[timestep, user_id, 0] = row["Latitude"]
            table[timestep, user_id, 1] = row["Longitude"]

    np.save(filename, table, allow_pickle=True, fix_imports=False)


# Load and save data
timestep_size = 60  # in seconds

trajectories = load_trajectories()
trajectories = convert_to_fixed_timesteps(trajectories, timestep_size)
save_numpy_matrix(trajectories)
print("Saved data in matrix.npy")
