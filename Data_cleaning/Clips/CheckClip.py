'''     take behavioral clip and apply bounding box on it, then save the newly created clip     '''


'''     imports     '''
import cv2
import pandas as pd
import os


'''     takes as input a clip path, it draws bounding boxes on top and creates new video with bounding box      '''
def getBBOXclip(clip_path, df_traj):

    # extract file path and clip name
    path, clip_name  = os.path.split(clip_path)

    # remove file extension
    clip_name = clip_name.replace(".MP4", "")

    # retrieve clip behavior, start time and stop time (this are referred to the file media)
    clip_b, clip_sa, clip_so = clip_name.split("_")

    # open clip with opencv
    cap = cv2.VideoCapture(clip_path)

    # retrieve width and height
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    size = (frame_width, frame_height)

    # result path
    result_path = path + "BBOX/" + clip_name + ".MP4"
    
    # resulting video parameters: name, fourcc, fps, size
    result = cv2.VideoWriter(result_path, 
                         -1,
                         29.97, size)


    count = 0

    txt = path + "BBOX/ListNoTrajectory.txt"

    no_bbox = True

    c = 0
    # open clip
    while cap.isOpened():

        # ret and frame
        ret, frame = cap.read() 

        # end the cycle if video ends or there is an issue, i.e. ret = False
        if not ret:
            break

        # time of the frame referred to file media: time of the clip + start time of the clip
        time = int(cap.get(cv2.CAP_PROP_POS_MSEC)/1000 + float(clip_sa))

        # bounding box were saved every 5 frames
        count_5 = int(count/5)
        
        #print(count, count_5, time)

        #print(df_traj[time == df_traj['time(s)']]['frame'])

        # if the frame has an annotation, draw bbox on the frame
        if df_traj[count_5 == df_traj['time_info']].empty == False:
            
            no_bbox = False
            c = c + 1
            
            # extract index
            #index = int(df_traj[df_traj['time_info']==count_5].index[0])
            index_list = df_traj[df_traj['time_info']==count_5].index.tolist()

            for index in index_list:

                # extract x, y center of bounding box, width and height
                x = df_traj['x'][index]
                y = df_traj['y'][index]
                w = df_traj['width'][index]
                h = df_traj['height'][index]

                x0 = int(x - w/2)
                y0 = int(y - h/2)
                x1 = int(x + w/2)
                y1 = int(y + h/2)

                # rectangle parameters
                # top left corner of rectangle
                start_point = (x0, y0)
                print(start_point)

                # bot right corner of rectangle
                end_point = (x1, y1)
                print(end_point)

                # colors
                color_r = (0, 255, 0)
                color_c = (0, 0, 255)

                # line thickness 
                thickness = 5

                # draw bbox on frame        
                frame = cv2.rectangle(frame, start_point, end_point, color_r, thickness)

                # draw center of bbox on frame
                frame = cv2.circle(frame, (int(x), int(y)), 5, color_c, thickness)
        
   
        # write frame in result file
        result.write(frame)
        
        # resize frames to be able to visualize well on your machine
        resize = cv2.resize(frame, (int(frame_width/4), int(frame_width/4)))

        # display the resulting frame
        cv2.imshow('My title',resize)
    
        # wait and exit if q is pressed
        if cv2.waitKey(30) == ord('q') or not ret:
            break

        # increase frame count
        count = count + 1          

    # if no bounding box is present on the clip
    if no_bbox:
        print(clip_path, ": no trajectory detected")

        # write txt file with clip name
        file = open(txt,"a")
        file.write(clip_name + "\n")

        # eliminate clip
        if os.path.exists(result_path):
            os.remove(result_path)
    
    print(c) 

    # when everything is done, release the capture
    cap.release() 
    cv2.destroyAllWindows()


'''     create all possible behavioral clips with bounding boxes from a given file media        '''
def getAll(video_path, df_association):
 
    # clips folder path
    index = video_path.find("G")
    video_name = video_path[index: -4]
    clips_path = video_path[:index - 1] + "/Clips/" + video_name + "/"


    # for every file in clip folder path check trajectories and creates clip
    for root, dirs, filenames in os.walk(clips_path, topdown=False):
        for filename in filenames:
            if ".MP4" in filename:
                clip_path = os.path.join(root, filename)
                

                if df_association[filename == df_association['Clip']].empty == False:
                    index = df_association[filename == df_association['Clip']].index.tolist()
                    traj_name = df_association['Unique_Name'][index[0]]
                    
                    behavior = traj_name[: traj_name.find("_")]


                    # trajectory csv paths
                    traj_path = "C:/Uni/Thesis/Thesis_Maybe/Data_cleaning/Trajectories/2022/Trajectories/" + behavior + "/" + traj_name

                    print(clip_path, traj_path)

                    # trajectory labels as dataframe
                    df_traj = pd.read_csv(traj_path)


                    getBBOXclip(clip_path, df_traj)



#video_path = "D:/Internship/Step1/Videos/2022/18.06/4/GH040081.MP4"
#getAll(video_path)
'''

# note: check Association Clip Media csv for matching behavioral clip and trajectory
clip_path = "D:/Internship/Step1/Videos/2022/18.06/4/Clips/GH040081/JS_122.2510000000002_127.MP4"
traj_path = "Trajectories/2022/Clips/JS/JS_0140.csv"

df_traj = pd.read_csv(traj_path)
getBBOXclip(clip_path, df_traj)
'''

#video_path =  "D:/Internship/Step1/Videos/2022/18.06/4/GH040081.MP4"
#asso_path = "C:/Uni/Thesis/Thesis_Maybe/Data_cleaning/Trajectories/2022/Association_Clip_Media.csv"
#df_association = pd.read_csv(asso_path)
#getAll(video_path, df_association)