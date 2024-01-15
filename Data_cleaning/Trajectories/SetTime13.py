'''     divide trajectories every 13 timestamps
        length of trajectories can vary        '''


'''     imports     '''
import pandas as pd
import os
import numpy as np
import math


'''     creates unique id for csv files
        input = behavior tag to find the correct folder
        output = unique 5 digits numeric id for the behavior
'''
def get_unique_id(behavior):

    # path folder of the csv files
    path_folder = "Trajectories/2022/SameLengthBeginning/" + behavior + "/"
    
    # for every file in the folder, append the unique int to a list
    list_int = []
    for root, dirs, filenames in os.walk(path_folder, topdown=False):
        for filename in filenames:

                # remove .csv
                filename = filename.replace(".csv", "")

                # find unique numeric id
                id = int(filename[filename.find('_') + 1:])

                # append the value
                list_int.append(id)

    # if there are alredy files in folder, find max value in the numeric id list
    if len(list_int) != 0:
        max_value = max(list_int)
    else:
        max_value = 0

    # add one
    new_value = str(max_value + 1)

    # add right zero padding to create a 5 digits unique id
    unique_id = new_value.rjust(5, "0")

    return unique_id


'''     save trajectory csv     
        inputs:
        - original filename
        - new df with trajectory of fixed length
        - new directory path        '''
def save_traj_csv(filename, df, n_path, df_traj_chunks):
    # extract behavior
    behavior = filename[:filename.find('_')]

    # extract unique id for the csv file
    unique_id = get_unique_id(str(behavior))

    # create unique name
    unique_name = str(behavior) + "_" + unique_id + ".csv"

    # create csv
    path_folder = n_path  + str(behavior) + "/"
    path_traj = n_path + str(behavior) + "/" + unique_name

    # if directory does not exist, create it
    if not os.path.exists(path_folder):
        os.mkdir(path_folder)

    traj_chunk = [filename, unique_name]
    df_traj_chunks.loc[len(df_traj_chunks)] = traj_chunk

    df.to_csv(path_traj, index=False)

    return df_traj_chunks
    


'''     divide trajectories every 13 timestamps and save csv files with newly create trajectories
        input:
        - trajectory path
        - fixed length
        - new trajectory path
        - csv to associate whole big trajectory and trajectories of length 13       '''
def set_same_len(path, fixed_len, n_path, df_traj_chunks):

    for root, dirs, filenames in os.walk(path, topdown=False):
        for filename in filenames:

            file_path = root + "/" + filename
            df = pd.read_csv(file_path)

            # if the maximum time info is smaller than the fixed value:
            # copy detections from 0 to fixed len
            if df['time_info'].max() < fixed_len-1:

                df_new = pd.DataFrame(columns=df.columns)

                # from 0 to fixed value (12)
                for index in range(fixed_len):
                    
                    # if the detection in the trajectory for the timestamp (a.k.a. index) is present,
                    # copy line from df
                    if df[index == df['time_info']].empty == False:
                        i = df[index == df['time_info']].index.tolist()    
                        df_new = df_new.append(df.loc[i])

                # save trajectory in csv file
                df_traj_chunks = save_traj_csv(filename, df_new, n_path, df_traj_chunks)

            # if the trajectory is greater than the fixed value:

            elif  df['time_info'].max() > fixed_len-1:

                # calculate ratio btw maximum time info and fixed length
                ratio = math.ceil(df['time_info'].max()/fixed_len)

                # create dictionary with how many dataframe as neeeded to cover the old df in chunks of fixed length
                dict_df = {}
                for i in range(ratio):
                    dict_df[i] = pd.DataFrame(columns=df.columns)


                # iterate in every new df
                # adding the detection/line when the timestamp has a detection in the original trajectory 
                for r in range(ratio):
                    for index in range(fixed_len):

                        # ind correspond to the timestamp
                        ind = index + fixed_len*r
                        
                        # copy line from df
                        if df[ind == df['time_info']].empty == False:
                            i = df[ind == df['time_info']].index.tolist()
                            dict_df[r] = dict_df[r].append(df.loc[i])

                # save trajectories in csv files                              
                for i in range(ratio):
                    df_traj_chunks = save_traj_csv(filename, dict_df[i], n_path, df_traj_chunks)


            else:
                # save trajectory in csv file
                df_traj_chunks = save_traj_csv(filename, df, n_path, df_traj_chunks)
            
            
    # save csv file with association trajectory name and trajectory of 13 detection (chunks) name
    df_traj_chunks.to_csv('Trajectories/2022/Association_Traj_Chunk.csv', index=False)
                
# original and new path            
path = "Trajectories/2022/Trajectories/"
n_path = "Trajectories/2022/SameLengthBeginning/"

# dataframe for associating trajectory name with chunks names
df_traj_chunks = pd.DataFrame(columns=['traj_name', 'chunk_name'])

# fixed length
fixed_len = 13

# set same length for every trajectory in the path
set_same_len(path, fixed_len, n_path, df_traj_chunks)

