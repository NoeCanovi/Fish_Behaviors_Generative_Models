'''     normalize the trajectories values to be in a range of [-1, 1]       '''

'''     imports     '''
import pandas as pd
import os


# path
trajectory_path = "Trajectories/2022/Interpolated"

# iterate over the csv files adding maximum and minimum values of each csv file
x_list = []
y_list = []
z_list = []

for root, dirs, filenames in os.walk(trajectory_path, topdown=False):
        for filename in filenames:
                file_path = root + "/" + filename
                df = pd.read_csv(file_path)

                x_list.append(df['x'].min())
                x_list.append(df['x'].max())

                y_list.append(df['y'].min())
                y_list.append(df['y'].max())

                z_list.append(df['ratio_wh'].min())
                z_list.append(df['ratio_wh'].max())

# extract maximum and minimum value for each component of the trajectory
x_max = max(x_list)
y_max = max(y_list)
z_max = max(z_list)

x_min = min(x_list)
y_min = min(y_list)
z_min = min(z_list)

print("MAX MIN")
print(x_max, x_min, y_max, y_min, z_max, z_min)


# normalize in a range between [-1, 1] (similar to UHAR preprocessing)
for root, dirs, filenames in os.walk(trajectory_path, topdown=False):
    for filename in filenames:
        file_path = root + "/" + filename
        df = pd.read_csv(file_path)
        df = df.drop('time_info',axis=1)

        new_x = []
        new_y = []
        new_z = []

        # add new values in the corresponding lists
        for x in df['x']:
            new_x.append(2*(x - x_min)/(x_max - x_min) - 1)
            
        for y in df['y']:
            new_y.append(2*(y - y_min)/(y_max - y_min) - 1)
            
        for z in df['ratio_wh']:
            new_z.append(2*(z - z_min)/(z_max - z_min) - 1)
        

        # convert the list to a dataframe and save it to a csv file
        new_df = pd.DataFrame(list(zip(new_x, new_y, new_z)), columns=df.columns)

        new_file_path = file_path.replace("Interpolated", "Normalized/SLB")

        if not os.path.exists(new_file_path.replace(filename, "")):
            os.mkdir(new_file_path.replace(filename, ""))


        new_df.to_csv(new_file_path, index=False)
        

