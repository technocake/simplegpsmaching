
import pandas as pd
import os


def load_trajectories(data_dir="Data/"):

	user_df_map = {}

 	# Loop over all data subdirectories
	for subdir, dirs, files in os.walk(data_dir):

		# Loop over all plt files
		for file in files:
			if not file.endswith(".plt"):
				continue

			# Convert plt files to pandas frame
			df = pd.read_csv(os.path.join(subdir, file), sep=',', 
				             skiprows=[0,1,2,3,4,5], usecols=[0,1,5,6],
				             names=["Longitude", "Latitude", "Date", "Time"], header=None)

			# Append trahectories to user
			user = int(subdir[5:8])
			if user in user_df_map:
				user_df_map[user] = user_df_map[user].append(df, ignore_index=True)
			else:
				user_df_map[user] = df

	return user_df_map
			

user_df_map = load_trajectories()

# Get trajectories of first user
user_df_map[0]

from IPython import embed; embed()