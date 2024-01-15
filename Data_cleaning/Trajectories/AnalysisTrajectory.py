'''     perform some analysis on trajectory csv     '''


'''     imports     '''
import os
import pandas as pd
import numpy as np
from collections import Counter
import statistics
from matplotlib import pyplot as plt


'''     return number of files in directory and subdirectories 
        note: counts only files, subfolders to not increment count      '''
def number_files(path): 
    file_number = sum([len(files) for r, d, files in os.walk(path)])
    return(file_number)


'''     return dictionary with behavior and number of file for subdirectory (behavior)       '''
def number_files_behavior(path):
    d = {}
    for root, dirs, filenames in os.walk(path, topdown=False):
        for dir in dirs:
            subdir_path = os.path.join(root, dir)
            d[dir] = number_files(subdir_path)
    sorted_d = dict(sorted(d.items(), key=lambda item: item[1]))

    return(sorted_d)


'''     return dictionary with trajectory that have more than one bounding box per frame
        with the number of duplicate frames        '''
def check_duplicate(path):
    d = {}

    # for every file in clip folder path check if there are more fish bounding boxes
    for root, dirs, filenames in os.walk(path, topdown=False):
        for filename in filenames:
            
            # read file as data frame
            file_path = os.path.join(root, filename)
            df = pd.read_csv(file_path)
            time_info = df['time_info']
            set_time_info = set(time_info)
            
            # if the set is less than the original, it means some duplicates have been eliminated
            if len(set_time_info) != len(time_info):
                d[filename] = len(time_info) - len(set_time_info)

    return d


'''     return list with trajectory unique name, media file and clip given one of the three     '''
def get_media_clip(line):
    # read csv as dataframe
    df_media = pd.read_csv("Trajectories/2022/Association_Clip_Media.csv")
    
    # if line is the unique name, extract other two variables
    if df_media[str(line) == df_media['Unique_Name']].empty == False:

        unique_name = line
        file_media = df_media.loc[df_media['Unique_Name'] == line,'Media'].values[0]
        clip = df_media.loc[df_media['Unique_Name'] == line,'Clip'].values[0]

    # else if line is the file media, extract other two variables
    elif df_media[str(line) == df_media['Media']].empty == False:

        unique_name = df_media.loc[df_media['Media'] == line,'Unique_Name'].values[0]
        file_media = line
        clip = df_media.loc[df_media['Media'] == line,'Clip'].values[0]

    # else if line is the clip, extract other two variables
    elif df_media[str(line) == df_media['Clip']].empty == False:

        unique_name = df_media.loc[df_media['Clip'] == line,'Unique_Name'].values[0]
        file_media = df_media.loc[df_media['Clip'] == line,'Media'].values[0]
        clip = line

    # return clip, file media and unique name
    return [clip, file_media, unique_name]


'''     analysis on clips with at least one frame with more than one bounding box       '''
def duplicate_analysis(d_dupl):

    # max, min, avg duplicate frames aka frames with more than one bounding box
    l_dupl = list(d_dupl.values())
    max_value = max(l_dupl)
    min_value = min(l_dupl)
    avg = sum(l_dupl)/len(l_dupl)
    print("max: ", max_value, ". min: ", min_value, ". avg: ", avg)

    # create list with clip, media, unique name for clips with at least 10 duplicate frames
    clip_media_un = []
    for key in d_dupl:
        if d_dupl[key] >= 10:
            media_clip = get_media_clip(key)
            clip_media_un.append(media_clip)

    # list with only file media
    media_list = [clip_media_un[i][1] for i in range (len(clip_media_un))]
    media_set = set(media_list)
    print("Number of clips with more than 10 duplicates frames (with and without repetition): ", len(media_list), ", ", len(media_set))

    # d counts how many time the same file media is present
    d =  Counter(media_list) 
    duplicates_media = [k for k, v in d.items() if v > 1]

    # sort list to make it more readable
    clip_media_un_sorted = sorted(clip_media_un, key=lambda x: x[1])

    # print every clip, media and unique name for every behavior that has more than 10 duplicate frames
    for i, l in enumerate(clip_media_un_sorted):
        if l[1] in duplicates_media:
            print(clip_media_un_sorted[i])
    return clip_media_un

'''     analysis on the lenght of the trajectories csv      '''
def lenght_analysis(traj_path, list_exclude):
    
    lenght_trajectories = []
    for root, dirs, filenames in os.walk(traj_path, topdown=False): 
        for filename in filenames:
            index = filename.find("_")
            behavior = filename[:index]
            if behavior not in list_exclude:
                path = root + "/" + filename
                df = pd.read_csv(path)
                lenght_trajectories.append(len(df))

    
    min_l_t = min(lenght_trajectories)
    max_l_t = max(lenght_trajectories)
    avg_l_t = sum(lenght_trajectories)/len(lenght_trajectories)
    median_l_t = statistics.median(lenght_trajectories)

    less_m = []
    for root, dirs, filenames in os.walk(traj_path, topdown=False): 
        for filename in filenames:
            path = root + "/" + filename
            df = pd.read_csv(path)
            if len(df) < median_l_t:
                less_m.append(len(df))


    print(min_l_t, max_l_t, avg_l_t, median_l_t)
    print("shorter than median:", len(less_m))

    num_bins = max(less_m)
    plt.hist(less_m, bins = num_bins)
    plt.show()

# trajectory folder
traj_path = "Trajectories/2022/Normalized/SLB"

# total number of trajectories csv
total_csv = number_files(traj_path)
print("total number of trajectories generated: ", total_csv)

# number of trajectories per behavior
d_beh = number_files_behavior(traj_path)
print("behavior and number of trajectories: ", d_beh)

#d = check_duplicate(traj_path)
#print(d)
#lenght_analysis(traj_path, [])


