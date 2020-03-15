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
            

def create_time_slots(trajectories, slot_size=60):
    """ Replaces the time column and  """

    def time_to_slot(row):
        h, m, s = map(int, row["Time"].split(':'))
        slot = round((h*3600+m*60+s)/slot_size)
        return slot

    for i, t in trajectories.items():
        t["Slot"] = t.apply(time_to_slot, axis=1)
        t = t.drop_duplicates("Slot")
        t = t.set_index("Slot")
        trajectories[i] = t
        
    return trajectories


# trajectories = load_trajectories()
# trajectories = create_time_slots(trajectories)
# # Get trajectories of first user
# #trajectories[0]

# from IPython import embed; embed()