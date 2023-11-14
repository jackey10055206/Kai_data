import pandas as pd
from datetime import *
from openpyxl import *
###########################

machine_num="1450"#機器代號
file_dir = "TG10-01450-2023-10-23T194200.data.txt"#你要用的data
real_time = "2023/10/25 20:51:10"#實際時間
machine_time = "2023/10/24 21:10:29"#機器時間
usecols = ['DATE','TIME','CO2','CH4']#你要抓的資料

Rtime = ["2023/10/25 15:54:50",
         "2023/10/25 16:02:50",
         "2023/10/25 16:14:10",
         "2023/10/25 16:24:30",
         "2023/10/25 16:34:00",
         "2023/10/25 16:44:50"] #實際時間
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
# data.to_excel("時間.xlsx",sheet_name="sheet1")
###########################


df = pd.read_csv(file_dir,sep='\s+',usecols=usecols) #把東西讀取進來

df_new = df.dropna() #如果有Nan就省略
print(df)