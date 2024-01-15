'''     create trajectories of fixed length and save them in csv files,
        when repeating detections, start from the beginning, e.g. ABCDAB        '''


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
def save_traj_csv(filename, df, n_path):
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

    # drop time information (was useful for interpolation, now not anymore)
    df = df.drop('time_info',axis=1)
    df.to_csv(path_traj, index=False)


'''     normalize trajectories of different length to fixed value
        input:
        - trajectory path
        - fixed length
        - new trajectory path       '''
def set_same_len(path, fixed_len, n_path):
    for root, dirs, filenames in os.walk(path, topdown=False):
        for filename in filenames:

            print(filename)
    
            file_path = root + "/" + filename
            df = pd.read_csv(file_path)

            # if the trajectory is smaller than the fixed value: 
            # repeat the dataframe and remove additional lines
            if len(df) < fixed_len:

                print("SMALLER")

                df_new = pd.DataFrame(columns=df.columns)

                for index in range(fixed_len):
                    ratio = math.floor(index/len(df))
                    # if index is in dataframe, copy the values
                    if index < len(df):
                        df_new.loc[len(df_new)] =  df.loc[index]

                    # else, repeat values from the beginning
                    else:
                        df_new.loc[len(df_new)] = df.loc[index - len(df)*ratio]                   

                # save trajectory in csv file
                save_traj_csv(filename, df_new, n_path)

            # if the trajectory is greater than the fixed value
            # divide in chunks of fixed length
            # if the last chunk is not of length of fixed length, repeat detections
            elif len(df) > fixed_len:

                print("LONGER")

                # calculateratio btw length of csv file and fixed length
                ratio = math.ceil(len(df)/fixed_len)

                # create dictionary with how many dataframe as neeeded to cover the old df in chunks of fixed length
                dict_df = {}
                for i in range(ratio):
                    dict_df[i] = pd.DataFrame(columns=df.columns)

                # iterate in every new df, adding one detection/line at the time in order to create 13 detections df
                for r in range(fixed_len):
                    for i in range(ratio):
                        index = r + fixed_len*i
    
                        # if index is in dataframe, copy the values
                        if index < len(df):
                            dict_df[i].loc[len(dict_df[i])] = df.loc[index]

                        # else, repeat values from the beginning
                        elif len(df) - fixed_len*(ratio-1) >= 6:
                            rat = math.ceil(index/len(df))
                            dict_df[i].loc[len(dict_df[i])] = df.loc[index - (len(df) - fixed_len*(i))*rat]

                # save trajectories in csv files                              
                for i in range(ratio):
                    if len(dict_df[i]) == fixed_len:
                        save_traj_csv(filename, dict_df[i], n_path)


            else:
                print("same length")

                # save trajectory in csv file
                save_traj_csv(filename, df, n_path)

                
            

path = "Trajectories/2022/Trajectories/"
n_path = "Trajectories/2022/SameLengthBeginning/"

fixed_len = 13
set_same_len(path, fixed_len, n_path)

