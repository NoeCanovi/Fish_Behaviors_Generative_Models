'''     divide dataset into train and test in a stratified way, 
        diving the whole big trajectories, not the 13-length ones       '''

'''     imports     '''
import pandas as pd
from sklearn.model_selection import train_test_split


# read csv with association btw original trajectories and trajectories of length 13
df = pd.read_csv('Trajectories/2022/Association_Traj_Chunk.csv')

# extract trajectory names and eliminate duplicate
traj_name = df['traj_name'].tolist()
set_traj_name = list(set(traj_name))

# for every trajectory, save its behavior
behavior_list = []
for traj_name in set_traj_name:
    behavior = traj_name[:traj_name.find('_')]
    behavior_list.append(behavior)

# extract number of trajectories and set train_size to 80% of it
data_length = len(set_traj_name)
train_size = int(0.8*data_length)

# create new dataframe with trajectory names and behaviors
new_df = pd.DataFrame(list(zip(set_traj_name, behavior_list)), columns=['traj_name', 'behavior'])

# divide trajectory in train and test
# stratify ensure the 80% ratio of train is true in every class of the dataset
x_train, x_test = train_test_split(new_df['traj_name'],  train_size=train_size, stratify=new_df['behavior'])

# copy set name (train or test) for every trajectory in the original dataframe
list_set = []
for traj in df['traj_name'].tolist():
    if traj in x_train.tolist():
        list_set.append('train')
    else:
        list_set.append('test')

# save csv file
new_df = pd.DataFrame(list(zip(df['traj_name'].tolist(), df['chunk_name'].tolist(), list_set)), columns=['traj_name', 'chunk_name', 'set'])
new_df.to_csv('Trajectories/2022/StratifiedDivisionDataset.csv', index=False)

