'''     create JS clips     
        note: used only for checking, if one wants to use it have to modify the paths and the id
'''


'''     imports     '''
import pandas as pd
from moviepy.editor import *
import math


'''     extract video path from aggregated behavior excel file        '''
def get_video_path(video_path):
    # Media file is saved as 'D:/Nest 2022/[month.day]/[camera_id]/G[H or X][video_id][other_numbers].MP4'
    # extract index of '2022'
    index = video_path.find("2022")

    # video path is everything from 2022 on
    v_path = video_path[index:]
    return(v_path)


'''     extract video path without video name from aggregated behavior excel file        '''
def get_path(video_path):
    # Media file is saved as 'D:/Nest 2022/[month.day]/[camera_id]/G[H or X][video_id][other_numbers].MP4'
    # extract indexes of '2022' and 'G'
    index0 = video_path.find("2022")
    index1 = video_path.find("G")

    # video path without file name
    v_path = video_path[index0:index1-1]
    return(v_path)

'''     extract video name without video path from aggregated behavior excel file        '''
def get_name(video_path):
    # Media file is saved as 'D:/Nest 2022/[month.day]/[camera_id]/G[H or X][video_id][other_numbers].MP4'
    # extract indexes of '2022' and 'G'
    index = video_path.find("G")

    # video path without file name
    v_name = video_path[index:]
    v_name = v_name.replace(".MP4", "")
    return(v_name)


'''     create behavior clips:
        video_path: path of the video
        df: dataframe with labels
        n_clip: number of clips to extract from the video'''
def create_clip(video_path, df, n_clip):

    # load video
    video = VideoFileClip(video_path)

    # extract media file columns and convert to string
    obs = df['Observation id'].tolist()

    # clip count is set to zero
    count = 0

    # for every line in the dataframe
    for i, ob in enumerate(obs):
        if ob == "2022 1806 Nest 4":
            start = df["Start (s)"][i]
            id = math.ceil(start/531.531)

            print(start, id)
            print(df["Observation id"][i])

  
            if id == 4:
                print(start, id)
                # save start and stop time
                start = df["Start (s)"][i] - (id-1)*531.531
                stop = df["Stop (s)"][i] - (id-1)*531.531

                # if start is less than 0, set to 0
                if start < 0:
                    start = 0

                # if stop is more than 531 (video length), set to 531
                elif stop > 531:
                    stop = 531
                
                # clip video
                print("start", start)
                print("stop", stop)

                
                clip = video.subclip(start, stop)


                # name of the clip = behavior + start time + stop time
                name_obs = "JS_" + str(start) + "_" + str(int(stop))

                
                #name_obs = name_obs.replace(".", "")

                # total clip_path
                # note: folders and subfolders have to exists already
                #clip_path = "D:/Internship/Step1/" + "Videos/" + path + "/Clips/" + name + "/" + name_obs + ".MP4"
                clip_path = "D:/Internship/Step1/Videos/2022/30.06/8/Clips/GH070023/" + name_obs + ".MP4"
                # remove audio
                clip = clip.without_audio()
                # save clip
                clip.write_videofile(clip_path)

                # clip count advance
                count = count + 1
                

            # if clip count is equal to number of clips wanted, break for cycle
            if count == n_clip:
                break
        

# path of the aggregated behavior excel file
label_path = 'Behavior/Excels/Male Inactive Time Stamps.xlsx'

# convert excel file to dataframe
df = pd.read_excel(label_path)

# create clips
create_clip("D:/Internship/Step1/Videos/2022/30.06/8/GH070023.MP4", df, 2)

