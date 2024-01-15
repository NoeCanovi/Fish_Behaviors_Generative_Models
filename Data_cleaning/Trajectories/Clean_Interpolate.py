'''     imports     '''
import pandas as pd
import os
import shutil
from scipy import interpolate
import matplotlib.pyplot as plt
import numpy as np
import math

'''     creates unique id for csv files
        input = behavior tag to find the correct folder
        output = unique 5 digits numeric id for the behavior
'''
def get_unique_id(behavior, n_path):

    # path folder of the csv files
    path_folder = n_path + behavior + "/"
    
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

    df_traj_chunks = pd.read_csv('Trajectories/2022/Association_Traj_Chunk.csv')

    # extract behavior
    behavior = filename[:filename.find('_')]

    # extract unique id for the csv file
    unique_id = get_unique_id(str(behavior), n_path)

    # create unique name
    unique_name = str(behavior) + "_" + unique_id + ".csv"

    # create csv
    path_folder = n_path  + str(behavior) + "/"
    path_traj = n_path + str(behavior) + "/" + unique_name

    # if directory does not exist, create it
    if not os.path.exists(path_folder):
        os.mkdir(path_folder)

    df.to_csv(path_traj, index=False)
    
    # substitute chunk from association trajetory name and chunk name file
    df_traj_chunks.loc[df_traj_chunks['chunk_name'] == filename, 'chunk_name'] = unique_name

    df_traj_chunks.to_csv('Trajectories/2022/Association_Traj_Chunk.csv', index=None) 


'''     clean directories:
        - delete trajectories csv dir which are not properly fish behavior
        - behaviors dir with only one trajectory      '''
def clean_directories(path):

    list_not_behavior = ['PS', 'FF']
    # all "present" events
    list_present = ['MP', 'FP', 'FP2', 'FP3', 'RP', 'GP', 'BP', 'IP', 'NNMP', 'ROP', 'BLP', 'MDP', 'PP', 'CRP', 'NOP']
    list_not_behavior = list_not_behavior + list_present

    # remove directories with same name as not behavior events
    for root, dirs, filenames in os.walk(path, topdown=False):
        for dir in dirs:
            dir_path = root + "/" + dir
            dir_len = sum([len(files) for r, d, files in os.walk(dir_path)])
            if dir in list_not_behavior or dir_len <= 1:
                
                # remove directory
                shutil.rmtree(dir_path)
                
              
    
'''     clean trajectories:
        - delete trajectory csv that have less or equal to 6 detection
        - delete trajectories csv which have duplicated frames aka more bounding boxes per frame      '''
def clean_trajectories(path):
    
    df_traj_chunks = pd.read_csv('Trajectories/2022/Association_Traj_Chunk.csv')

    for root, dirs, filenames in os.walk(path, topdown=False):
        for filename in filenames:
    
            file_path = root + "/" + filename

            # read trajectory file as dataframe
            df = pd.read_csv(file_path)
            time_info = df['time_info']
            set_time_info = set(time_info)
            
            # if the set is less than the original, it means some duplicates are present
            if len(set_time_info) != len(time_info) or len(time_info) <= 6:
                os.remove(file_path)

                # remove behavior from association trajetory name and chunk name file
                if df_traj_chunks[filename == df_traj_chunks['chunk_name']].empty == False:
                        index = df_traj_chunks[filename == df_traj_chunks['chunk_name']].index.tolist()
                        df_traj_chunks = df_traj_chunks.drop(index[0])
    

    df_traj_chunks.to_csv('Trajectories/2022/Association_Traj_Chunk.csv', index=None)        

          


'''     spline interpolation     
        inputs:
        - t = time information
        - x, y = center of bbox
        - r = ratio
        - plot = boolean to indicate to plot or not data
    
        outputs:
        - yfit[0] = interpolated x
        - yfit[1] = interpolated y
        - yfit[2] = interpolated r
'''
def direct_spline_interpolation(t, x, y, r, plot=False):

    tck, u = interpolate.splprep([x,y,r], s=0, u = t, k = 1)
   
    # u_new = t_new = all values from first time info value to last time info value
    #u_new = np.arange(t[0], t[-1]+1, 1)
    t_begin = math.floor(t[0]/13)*13
    t_end = t_begin + 13
    u_new = np.arange(t_begin, t_end , 1)

    # evaluate the spline and get new values
    yfit = interpolate.splev(u_new, tck)
    
    
    '''
    plt.plot(t, x, 'ro')
    plt.plot(u_new, yfit[0],'b')
    plt.title("Direct spline interpolation")
    plt.show()
    '''

    return yfit[0], yfit[1], yfit[2]


'''     interpolate all trajectories csv from a given path        '''
def interpolate_all(path):
    for root, dirs, filenames in os.walk(path, topdown=False):
        for filename in filenames:
            
            # read trajectory file as dataframe
            file_path = root + "/" + filename
            df = pd.read_csv(file_path)

            # extract time info value
            t = df['time_info'].tolist()

            # extract all time values
            #new_t = np.arange(t[0], t[-1]+1, 1)
            t_begin = math.floor(t[0]/13)*13
            t_end = t_begin + 13
            new_t = np.arange(t_begin, t_end , 1)
            
            
            # if the two differs, it means the trajectories has missing detections
            if len(t) < len(new_t):
                
                print(filename)
                # extract x, y center of bbox and ratio w/h from csv
                x = df['x'].to_list()
                y = df['y'].to_list()
                r = df['ratio_wh'].to_list()

                # apply spline interpolation
                new_x, new_y, new_r = direct_spline_interpolation(t, x, y, r)

                # create new df and replace old trajectory
                new_df = pd.DataFrame(list(zip(new_t, new_x, new_y, new_r)), columns=df.columns)

                # subsitute old csv
                # save trajectory in csv file
                n_path = "Trajectories/2022/Interpolated/"
                save_traj_csv(filename, new_df, n_path)

                
    
            else:
                n_path = "Trajectories/2022/Interpolated/"
                save_traj_csv(filename, df, n_path)
            
            

path = "Trajectories/2022/SameLengthBeginning"
clean_directories(path)
clean_trajectories(path)
#interpolate_all(path)
