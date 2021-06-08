import requests
import csv
import json
import pandas as pd
import numpy as np
from pandas import json_normalize

train_info_july = list()

for day in range(1, 32):
    train_info = requests.get(
        f'https://rata.digitraffic.fi/api/v1/trains/2020-07-{"0" + str(day) if day // 10 == 0 else str(day)}/4')
    train_info_july.extend(train_info.json())
df = json_normalize(train_info_july,"timeTableRows",["trainNumber", "departureDate"])
df.to_csv('train_4_2020_07.csv', index=False)
actual_time = pd.DataFrame(df[df['stationShortCode']=='HKI']['actualTime'].apply(str.split, args=('T')).tolist())[1]
actual_time_int64 = pd.to_datetime(actual_time).values.astype(np.int64)

avg_actual_time = pd.to_datetime(actual_time_int64.mean())
avg_actual_time = avg_actual_time.time()
with open('train_4_2020_07_avg_actual_time.txt', 'w') as txtfile:
    txtfile.write(str(avg_actual_time))
