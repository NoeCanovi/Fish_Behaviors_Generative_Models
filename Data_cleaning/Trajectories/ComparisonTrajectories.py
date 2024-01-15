'''     plot trajectories       '''

'''     imports     '''
import matplotlib.pyplot as plt
import pandas as pd


'''
df_1 = pd.read_csv('Trajectories/2022/Interpolated/C/C_00059.csv')
df_3 = pd.read_csv('Trajectories/2022/InterpolatedD3/C/C_00059.csv')
df = pd.read_csv('Trajectories/2022/SameLengthBeginning/C/C_00080.csv')


df_1 = pd.read_csv('Trajectories/2022/Interpolated/JS/JS_00041.csv')
df_3 = pd.read_csv('Trajectories/2022/InterpolatedD3/JS/JS_00041.csv')
df = pd.read_csv('Trajectories/2022/SameLengthBeginning/JS/JS_00241.csv')
'''

''' read csv as dataframes:
    df_1 = interpolated with liner spline
    df_3 = interpolated with cubic spline (default)
    df   = original data
'''
df_1 = pd.read_csv('Trajectories/2022/Interpolated/JS/JS_00088.csv')
df_3 = pd.read_csv('Trajectories/2022/InterpolatedD3/JS/JS_00088.csv')
df = pd.read_csv('Trajectories/2022/SameLengthBeginning/JS/JS_00459.csv')

# extract time and x of the original dataframe
to = df['time_info']
x = df['x']

# range of time values, should be multiple of 13. Needs to be adjusted depending on the csv.
t = range(26, 39, 1)

# extract x from the two interpolated trajectories
x_1 = df_1['x']
x_3 = df_3['x']

# plot trajectories
plt.plot(to, x, 'ro')
plt.plot(t, x_1, 'g', label='Degree 1')
plt.plot(t, x_3, 'b', label='Degree 3')
plt.legend()
plt.title("Spline interpolation")
plt.show()