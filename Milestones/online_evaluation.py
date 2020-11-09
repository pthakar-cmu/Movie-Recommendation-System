import pandas as pd
import numpy as np

'''
Note: logs.csv is orginally on server. Use scp to copy to local.
'''

# sometimes logs are written in the same line as the previous one, so use first 23 columns
logs = pd.read_csv('logs.csv', header=None, usecols=list(range(23)))
logs.columns = ['time', 'user_id', 'latency'] + [str(i) for i in range(1, 21)]

# calculate average latency
latency = {}
latency['avg'] = logs['latency'].mean()
latency['std'] = logs['latency'].std()
latency['max'] = logs['latency'].max()
latency['min'] = logs['latency'].min()
latency['q_90'] = logs['latency'].quantile(0.9)

# calculate number of requests per unit
avg_req = {}
times = list(logs['time'] - logs.loc[0, 'time'])
bins_min = list(range(times[0], times[-1], 60))
avg_req['minute'] = np.histogram(times, bins=bins_min)[0].mean()
bins_hr = list(range(times[0], times[-1], 3600))
avg_req['hour'] = np.histogram(times, bins=bins_hr)[0].mean()

# write online evaluation report
with open('online_evaluation_report.txt', 'w') as file:
    file.write('********** Online Metric Report **********')
    file.write('\n\n')
    file.write('***** Latency *****')
    file.write('\n\n')
    file.write('Mean: \t\t\t' + str(round(latency['avg'], 2)) + 'ms\n')
    file.write('Std: \t\t\t' + str(round(latency['std'], 2)) + '\n')
    file.write('Max: \t\t\t' + str(round(latency['max'], 2)) + 'ms\n')
    file.write('Min: \t\t\t' + str(round(latency['min'], 2)) + 'ms\n')
    file.write('90% quantile: \t' + str(round(latency['q_90'], 2)) + 'ms\n')
    file.write('\n')
    file.write('***** Number of requests *****')
    file.write('\n\n')
    file.write('Per minute: ' + str(round(avg_req['minute'], 2)) + '\n')
    file.write('Per hour: \t' + str(round(avg_req['hour'], 2)) + '\n')
