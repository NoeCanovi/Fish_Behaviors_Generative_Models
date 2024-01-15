'''     extract and print max, min values of trajectories given file path       '''

'''     imports     '''
import pandas as pd
import os

# path
trajectory_path = "Trajectories/2022/Trajectories"

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


x_max = max(x_list)
y_max = max(y_list)
z_max = max(z_list)

x_min = min(x_list)
y_min = min(y_list)
z_min = min(z_list)

print("MAX MIN")
print(x_max, x_min, y_max, y_min, z_max, z_min)

