'''     extract class weight for focal loss     '''
'''     imports     '''

import pandas as pd
import os


'''     return number of files in directory and subdirectories 
        note: counts only files, subfolders to not increment count      '''
def number_files(path): 
    file_number = sum([len(files) for r, d, files in os.walk(path)])
    return(file_number)

# classes
classes = ['C', 'EP', 'FD', 'FM', 'GC', 'JS', 'MA', 'MR', 'NB','NFM', 'S', 'SSP']
num_classes = 12

total_samples = number_files('Trajectories/2022/Divided/train/')

# for each class, calculate weight
class_weights = []
for c in classes:
    c_path = 'Trajectories/2022/Divided/train/' + c
    count = number_files(c_path)
    weight = 1/ (count /total_samples)
    class_weights.append(weight)


# convert in dataframe and save csv with class and weight
df = pd.DataFrame(list(zip(classes, class_weights)), columns=['class', 'weight'])
df.to_csv('train_class_weight.csv', index=False)
