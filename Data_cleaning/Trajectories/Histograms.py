'''     create histograms with trajectory lengths       '''


'''     imports     '''
import pandas as pd
from matplotlib import pyplot as plt
import os


'''     get length trajectories      '''
def length_traj(path):
    length_list = []
    for root, dirs, filenames in os.walk(path, topdown=False):
        for filename in filenames:
    
            file_path = root + "/" + filename
            df = pd.read_csv(file_path)
            length_list.append(len(df))

    return length_list


# trajectory path
path = "Trajectories/2022/SameLengthBeginning"

# get lengths
length_list = length_traj(path)

# show histogram
num_bins = max(length_list)
plt.hist(length_list, bins = num_bins)
plt.show()
