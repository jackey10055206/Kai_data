import pandas as pd
import numpy as np
from datetime import *
from openpyxl import *
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
###########################

machine_num="1205"#機器代號
file_dir = "TG20-01205-2023-10-28T080000.data.txt"#你要用的data
real_time = "2023/10/25 20:28:32"#實際時間
machine_time = "2023/10/25 20:32:58"#機器時間
usecols = ['DATE','TIME','N2O']#你要抓的資料(記得要改格式)
Rtime = ["2023/10/25 10:30:50",
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

df_new['TIME']= pd.to_datetime(df_new['TIME'], format='%H:%M:%S',errors= 'coerce').dt.time#把TIME那欄換成datetime

#print(df_new['TIME'])


start_time = pd.to_datetime(Mtime[0])
end_time = start_time + timedelta(minutes=3)

selected_data = df_new[(df_new["TIME"] > start_time.time()) & (df_new["TIME"]< end_time.time())]

#print(selected_data)

############################################################
regression_results = []

for i in range(len(selected_data) - 60):
    window_data = selected_data['N2O'].iloc[i:i + 60].values.reshape(-1, 1)
    window_time = np.arange(60).reshape(-1, 1)

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


