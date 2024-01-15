'''     copy csv files in correct folder depending on set name (train or test)'''

'''     imports     '''
import os
import shutil
import pandas as pd

# read csv with set infomration as dataframe
df = pd.read_csv('Trajectories/2022/StratifiedDivisionDataset.csv')

# for every file in the path, copy csv file in correct folder
path = 'Trajectories/2022/Normalized/SLB'
for root, dirs, filenames in os.walk(path, topdown=False):
        for filename in filenames:    
            file_path = root + "/" + filename

            # extract set name from dataframe and behavior
            s = df.loc[df['chunk_name'] == filename, 'set'].values[0]
            behavior = filename[:filename.find("_")]

            path_folder = 'Trajectories/2022/Divided/' + s + "/" + behavior + "/"
        
            # if directory does not exist, create it
            if not os.path.exists(path_folder):
                os.mkdir(path_folder)
            
            # copy csv file
            shutil.copy(file_path, path_folder + filename)
            