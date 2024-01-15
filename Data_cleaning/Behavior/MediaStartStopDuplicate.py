'''     Create xlsx file with added columns:
        - id: order of the media in the total file
        - M_Start: start of the event referred to the media file video
        - M_Stop: stop of the event referred to the media file video
'''


'''     imports     '''
import pandas as pd


'''     extract video id from aggregated behavior excel file        '''
def get_video_id(video_path):
    # Media file is saved as 'D:/Nest 2022/[month.day]/[camera_id]/G[H or X][video_id][other_numbers].MP4'
    # extract index of 'G'
    index = video_path.find("G")

    # video id is the two digits after GH or GX
    v_id = video_path[index + 2: index + 4]
    return(v_id)


'''     extract video path from aggregated behavior excel file        '''
def get_video_path(video_path):
    # Media file is saved as 'D:/Nest 2022/[month.day]/[camera_id]/GH[video_id][other_numbers].MP4'
    # extract index of '2022'
    index = video_path.find("2022")

    # video id is the two digits after GH
    v_path = video_path[index:]
    return(v_path)


'''     extract id from aggregated behavior excel file, and save ids to a column of a dataframe      '''
def id(data):

    # convert excel file to dataframe
    df = pd.read_excel(label_path)

    # extract media file column and convert it to strings
    media_file = df['Media file']
    media_file_str = [str(i) for i in media_file]

    # extract id for every line of the column and add ids to a list
    id_list = []
    for i, string in enumerate(media_file_str):
        
        id = get_video_id(string)
        id = float(id)
        id_list.append(id)

    # create new data frame with added column "ID" and with ids as values
    df_id = df.assign(ID = id_list)
    return df_id       

# path of the old excel file
label_path = 'Behavior/Excels/Aggregated Behaviours - Ben Ellis.xlsx'

# create new dataframe with the above file and the added columns "ID"
df_id = id(label_path)

# extract id, start and stop columns
id = df_id["ID"]
start = df_id["Start (s)"]
stop = df_id["Stop (s)"]

# m_start and m_stop are list with the new start and stop values
m_start = []
m_stop = []
stop_next_list = []
for i, id_obs in enumerate(id):

    # id_obs starts from 1, and every video (but the last of the sequence) has same length 531.5310000000001
    start_observation = start[i] - (id_obs - 1)*531.5310000000001
    stop_observation = stop[i] - (id_obs - 1)*531.5310000000001

    # if stop value is above 531, create duplicate annotation
    if stop_observation > 531:
        
        # duplcicate stop value
        stop_next = stop_observation - 531

        # extract row as dataframe
        line = df_id.iloc[[i]]

        # duplicate media value (add 1 to the id)
        old_media_value = str(line.iloc[0]['Media file'])
        index = old_media_value.find("G")

        if id_obs < 9:
            new_media_value = old_media_value[: index + 3] + str(int(id_obs + 1)) + old_media_value[index + 4:]
        else:
            new_media_value = old_media_value[: index + 2] + str(int(id_obs + 1)) + old_media_value[index + 4:]
      
        line['Media file'] = new_media_value
        line['M_Start'] = 0
        line['M_Stop'] = stop_next
        line['ID'] = int(id_obs + 1)

        stop_next_list.append(stop_next)

        df_id = pd.concat([df_id, line], ignore_index=True)
    
        stop_observation = 531


    m_start.append(start_observation)
    m_stop.append(stop_observation)


m_start = m_start + [0] * (len(df_id) - len(m_start))
m_start = m_start + [0] * (len(df_id) - len(m_start))
m_stop = m_stop + stop_next_list


# create new data frame with two new columns (M_Start and M_Stop)
df_times = df_id.assign( M_Start = m_start)
df_times = df_times.assign( M_Stop = m_stop)

# sort dataframe
df_sorted = df_times.sort_values(["Media file", "M_Start"])

# create excel file with the new dataframe
df_sorted.to_excel('Behavior/Excels/AB_Media.xlsx')
