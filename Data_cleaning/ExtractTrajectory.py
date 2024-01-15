'''     creates a csv per behavior event with: behavior, new_time, x, y, w, h, wh ratio       '''


'''     imports     '''
import pandas as pd
import os


'''     returns the trajectory of the media from which the clip has been extracted
        input example = "D:/Nest 2022/18.06/4/GH040081.MP4"
        the input can be extracted by AB_Media file
        output = trajectory path
'''
def get_trajectory_path(line):

    # find indices to remove unnecessary parts
    index_0 = line.find("2022")
    index_1 = line.find("G")
    line = line[index_0:index_1 - 1]

    # extract year, date and camera
    year, date, camera = line.split("/")
    day, month = date.split(".")

    # trajectory path
    traj_path = "Trajectories/csv_Vaneeda/Merged_" + year + month + day + "_" + camera + ".csv"
    return traj_path


'''     creates unique id for csv files
        input = behavior tag to find the correct folder
        output = unique 4 digits numeric id
'''
def get_unique_id(behavior):

    # path folder of the csv files
    path_folder = "Trajectories/2022/Clips/" + behavior + "/"
    
    # for every file in the folder, append the unique int to a list
    list_int = []
    for root, dirs, filenames in os.walk(path_folder, topdown=False):
        for filename in filenames:

                # remove .csv
                filename = filename.replace(".csv", "")

                # find when the unique numeric id starts (name = behavior tag + _ + unique id)
                index = filename.find('_')
                id = int(filename[index + 1:])

                # append the value
                list_int.append(id)

    if len(list_int) != 0:
         # find max value in the list
        max_value = max(list_int)
    else:
        max_value = 0
   

    # add one
    new_value = str(max_value + 1)

    # add right zero padding to create a 4 digits unique id
    unique_id = new_value.rjust(4, "0")

    return unique_id


'''     create csv file for every clip in file media
        file media = kist of paths of media file
        
        if more than one track on same clip, create different dataframe
'''
def create_trajectory(file_media, df_durations):


    # create dataframe in order to correlate clip name, media file name and unique name
    media_clip = pd.DataFrame(columns=['Clip', 'Media', 'Unique_Name'])

    # file media has many duplicate, create a set to eliminate these
    file_media = set(file_media)

    # loop for every file media (video)
    for e, media in enumerate(file_media):

        # extract trajectory path
        traj_path = get_trajectory_path(media)

        # check if the trajectory exists
        traj_exist = os.path.exists(traj_path)

        # if it exists: create csv for every clip in the video with corresponding trajectory
        # if it does not: do nothing
        if traj_exist:

            # read trajectory csv as dataframe
            df_traj = pd.read_csv(traj_path)

            # extract all row indices that have the media in Media file column
            index = df_ab[df_ab['Media file']==media].index.tolist()

            # for every of these indices, extract useful information from row
            for i in index:

                # extract start, stop, behavior, id of the video and fps
                m_start = df_ab.iloc[i]['M_Start']
                m_stop = df_ab.iloc[i]['M_Stop']
                behavior = df_ab.iloc[i]['Behavior']
                id_video = df_ab.iloc[i]['ID']
                fps = float(df_ab.iloc[i]['FPS'])

                #print(m_start, m_stop, behavior, id_video, fps)

                # check if start and stop are equal, this mean this is a point event
                # so equal time is added before and after                
                if m_start == m_stop:
                    
                    try:
                        index = df_durations[df_durations['Behavior code']==behavior].index.tolist()
                        duration = df_durations['Average Duration (Seconds)'][index[0]]
                    except:
                        duration = 0
                        print(behavior, "BEHAVIOR NO DURATION")
                        
                    added_time = int(duration/2)
                    m_start = m_start - added_time
                    m_stop = m_stop + added_time

                # if start is less than 0, set to 0
                if m_start < 0:
                    m_start = 0

                # if stop is more than 531 (video length), set to 531
                elif m_stop > 531:
                    m_stop = 531    

                # original video is at 29.97 or 59.94 fps
                # trajectory video frames are instead extracted and saved every 5 frames
                # to match the trajectory csv: frame = time*(fps/5)
                # in addition, frames refer to a concatenation of media file
                # to match the trajectory, add frames equal to media lenght*fps/5
                # and multiplied by the order (minus 1) (i.e. id) of the media in the concatenation
                frame_start = (m_start*fps)/5 + (id_video - 1)*(531.531)*(fps/5)
                frame_stop = (m_stop*fps)/5 + (id_video - 1)*(531.531)*(fps/5)

                #print(frame_start, frame_stop)

                # create list with all frames from starting to ending frame
                frames = [i for i in range(int(frame_start), int(frame_stop + 1))]


                # collect time information
                # it will change every 5 original video frames, i.e. every "frame" here
                new_time = 0

                # create dataframes in which we can save the trajectory of the clip and other information
                df_clip = pd.DataFrame(columns=['behavior', 'time_info', 'x', 'y', 'width', 'height', 'ratio', 'track'])

                # create dataframes in which we can save the trajectory of the clip
                df_traj_clip = pd.DataFrame(columns=['time_info','x', 'y', 'ratio_wh'])
               
                # for every frame of the clip/trajectory
                for frame in frames:
                    
                    # check if the corresponding frame is present in the trajectory dataframe
                    if df_traj[frame == df_traj['frame']].empty == False:
                        #print(frame)

                        #print(traj_path)

                        # extract indeces when the frame is present
                        # multiple indices means there are more bounding box, i.e. fish in the frame
                        index = df_traj[df_traj['frame']==frame].index.tolist()

                        #print(index)

                        # for every index found
                        for i_0 in index:

                            # extract x0, y0, x1, y1, i.e top-left corner and bot-right corner, and time
                            x0 = df_traj['x0'][i_0]
                            y0 = df_traj['y0'][i_0]
                            x1 = df_traj['x1'][i_0]
                            y1 = df_traj['y1'][i_0]
                            #time = df_traj['time(s)'][i] - (531.531)*(id_video - 1)
                            track = df_traj['track'][i_0]

                            # width, height and ratio of the bounding box
                            w = x1 - x0
                            h = y1 - y0
                            wh = w/h

                            # center of bounding box
                            x = x0 + w/2
                            y = y0 + h/2

                            # list of relevant values
                            list = [behavior, new_time, x, y, w, h, wh, track]

                            # add those in df_clip dataframe
                            df_clip.loc[len(df_clip)] = list

                            # list of trajectory data: time information, x, y, ratio w/h
                            traj = [new_time, x, y, wh]

                            # add those in df_traj_clip
                            df_traj_clip.loc[len(df_traj_clip)] = traj
                
                            # converting time info to int (it is automatically saved as float even if it is int)
                            df_traj_clip['time_info'] = df_traj_clip['time_info'].astype(int)


                    # increase time count
                    new_time = new_time + 1

                # extract unique id for the csv file
                unique_id = get_unique_id(str(behavior))

                # create unique name
                unique_name = str(behavior) + "_" + unique_id + ".csv"

                # create csv
                path_folder = "Trajectories/2022/Clips/" + str(behavior) + "/"
                path_clip = "Trajectories/2022/Clips/" + str(behavior) + "/" + unique_name

                if not df_clip.empty:
                    if os.path.exists(path_folder):
                        df_clip.to_csv(path_clip, index=False)
                    else:
                        os.mkdir(path_folder)
                        df_clip.to_csv(path_clip, index=False)

                path_folder = "Trajectories/2022/Trajectories/" + str(behavior) + "/"
                path_csv = "Trajectories/2022/Trajectories/" + str(behavior) + "/" + unique_name

                if not df_traj_clip.empty:
                    if os.path.exists(path_folder):
                        df_traj_clip.to_csv(path_csv, index=False)
                    else:
                        os.mkdir(path_folder)
                        df_traj_clip.to_csv(path_csv, index=False)
     

                #print("path_csv", path_csv)
                if not df_traj_clip.empty:
                    name_clip = str(behavior) + "_" + str(m_start) + "_" + str(int(m_stop)) + ".MP4"
                    # add media file and name of the clip to media clip csv
                    media_clip_list = [name_clip, media, unique_name]
                    media_clip.loc[len(media_clip)] = media_clip_list

            

    # save csv with clip and media
    media_clip.to_csv("Trajectories/2022/Association_Clip_Media.csv" , index=False)


# read aggregated behavior excel
ab_path = "Behavior/Excels/AB_Media.xlsx"
df_ab = pd.read_excel(ab_path)
file_media = df_ab["Media file"]

df_durations = pd.read_excel("Behavior/Excels/Average Duration.xlsx")
create_trajectory(file_media, df_durations)