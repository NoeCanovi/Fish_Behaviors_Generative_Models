'''     create behavioral clips     '''


'''     imports     '''
import pandas as pd
from moviepy.editor import *


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
def create_clip(video_path, df, df_durations, n_clip, beh_list):

    # load video
    video = VideoFileClip(video_path)

    # extract video path
    v_path = get_video_path(video_path)

    # extract media file columns and convert to string
    media_file = df['Media file']
    media_file_str = [str(i) for i in media_file]

    # clip count is set to zero
    count = 0

    # for every line in the dataframe
    for i, string in enumerate(media_file_str):
        
        # if the video is contained in the media file column of the label, i.e. if the observations are referred to the video
        if v_path in string:

            print(df['Behavior'][i])
            if df['Behavior'][i] in beh_list:
                # save start and stop time
                start = df["M_Start"][i]
                stop = df["M_Stop"][i]

                # in case of point event, i.e. start == stop, create 10 seconds clip by adding 5 sec before and after the middle point 
                if start == stop:
                    
                    try:
                        index = df_durations[df_durations['Behavior code']==df['Behavior'][i]].index.tolist()
                        duration = df_durations['Average Duration (Seconds)'][index[0]]

                    except:
                        duration = 5
                        print(df['Behavior'][i], " is missing average duration")


                    added_time = duration/2

                    print(added_time)
                    start = start - added_time
                    stop = stop + added_time

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
                
                # extract path  and name of the video
                path = get_path(video_path)
                name = get_name(video_path)

                # name of the clip = behavior + start time + stop time
                name_obs = str(df["Behavior"][i]) + "_" + str(start) + "_" + str(int(stop))

                
                #name_obs = name_obs.replace(".", "")

                # total clip_path
                # note: folders and subfolders have to exists already
                clip_path = "D:/Internship/Step1/" + "Videos/" + path + "/Clips/" + name + "/" + name_obs + ".MP4"

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
path_AB = 'Behavior/Excels/AB_Media.xlsx'

# convert excel file to dataframe
df = pd.read_excel(path_AB)

# list behaviors to extract
behavior = ['EP']

# path of the average point behavior duration
df_durations = pd.read_excel('Behavior/Excels/Average Duration.xlsx')

# create clips
create_clip("D:/Internship/Step1/Videos/2022/18.06/4/GH070081.MP4", df, df_durations, 3, behavior)