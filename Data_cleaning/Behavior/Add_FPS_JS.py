'''     add FPS column to Male Inactive Time Stamps excel, by taking the values from Aggregated Behaviors excel     '''

'''     imports     '''
import pandas as pd


# read excels as dataframes
df_ab = pd.read_excel("Behavior/Excels/Aggregated Behaviours - Ben Ellis.xlsx")
df = pd.read_excel("Behavior/Excels/Male Inactive Time Stamps.xlsx")

fps = df_ab['FPS']
fps_new = []

obs = df['Observation id']
for i, ob in enumerate(obs):

    # replace "Nest" with "Cam"
    ob = ob.replace("Nest", "Cam")

    # check if the observation id exists in df_ab and append fps value to fps list
    if df_ab[ob == df_ab['Observation id']].empty == False:
        index = df_ab[df_ab['Observation id']== ob].index.tolist()
        
        f = float(df_ab.iloc[index[0]]['FPS'])
        
        fps_new.append(f)


# add column to dataframe
df['FPS'] = fps_new

# convert dataframe to excel
df.to_excel("Behavior/Excels/JS.xlsx")
