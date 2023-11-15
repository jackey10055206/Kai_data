import pandas as pd
import numpy as np
from datetime import *
from openpyxl import *
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
###########################

machine_num="1205"#機器代號
file_dir = "TG10-01450-2023-10-23T194200.data.txt"#你要用的data
real_time = "2023/10/25 20:51:10"#實際時間
machine_time = "2023/10/24 20:38:21"#機器時間
usecols = ['DATE','TIME','CH4']#你要抓的資料(記得要改格式)
Rtime = ["2023/10/25 15:54:50",
         "2023/10/25 11:04:10",
         "2023/10/25 11:12:00",
         "2023/10/25 12:03:10",
         "2023/10/25 12:09:55",
         "2023/10/25 12:19:15"] #實際時間
###########################

date1 = datetime.strptime(real_time,"%Y/%m/%d %H:%M:%S")
date2 = datetime.strptime(machine_time,"%Y/%m/%d %H:%M:%S")

duration = date1 - date2

Mtime = []
for i in range(6):
    tmp = (datetime.strptime(Rtime[i],"%Y/%m/%d %H:%M:%S")) - (duration)
    Mtime.append(str(tmp))


col1='機器時間'
col2='實際時間'
data = pd.DataFrame({col1: Mtime,col2: Rtime})
#print(data)
# data.to_excel("時間.xlsx",sheet_name="sheet1")
###########################


df = pd.read_csv(file_dir,sep='\s+',usecols=usecols) #把東西讀取進來

df_new = df.dropna() #如果有Nan就省略

df_new['TIME'] = pd.to_datetime(df_new['TIME'], format='%H:%M:%S',errors= 'coerce').dt.time#把TIME那欄換成datetime
df_new['DATE'] = pd.to_datetime(df_new['DATE'], format='%Y-%m-%d',errors='coerce')

df_new['DATETIME'] = pd.to_datetime(df_new['DATE'].astype(str) + ' ' + df_new['TIME'].astype(str),errors='coerce')
#print(df_new['DATETIME'])

start_time = pd.to_datetime(Mtime[0])

end_time = start_time + timedelta(minutes=3,seconds=1)

selected_data = df_new[(df_new["DATETIME"] > start_time) & (df_new["DATETIME"]< end_time)]


print(selected_data)

############################################################
regression_results = []

for i in range(len(selected_data) - 120):
    window_data = selected_data['CH4'].iloc[i:i + 120].values.reshape(-1, 1)
    window_time = np.arange(120).reshape(-1, 1)

    model = LinearRegression()
    model.fit(window_time, window_data)

    a, b = model.coef_[0][0], model.intercept_[0]

    predicted_values = model.predict(window_time)
    r2 = r2_score(window_data, predicted_values)

    # 存储结果
    regression_results.append({'start_time': selected_data['TIME'].iloc[i], 'a': a, 'b': b, 'r2': r2})

# 将结果转换为DataFrame
result_df = pd.DataFrame(regression_results)
print(result_df)
############################################################


