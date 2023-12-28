# process_data.py

# 人工輸入區
machine_num = "1696"  # 機器代號
machine_series = "JZ4"  # 採樣地點
file_dir = "TG10-01450-2023-10-23T194200.data.txt"  # 你要用的 data
usecols = ['DATE', 'TIME', 'CO2']  # 你要抓的資料(記得要改格式)
gas_column = ['CO2']  # 你要抓的資料(記得要改格式)
Real_time = "2023/10/25 20:51:10"  # 實際時間
Machine_time = "2023/10/24 21:10:29"  # 機器時間
Rtime = ["2023/10/25 15:54:50",
         "2023/10/25 16:02:50",
         "2023/10/25 16:14:10",
         "2023/10/25 16:24:30",
         "2023/10/25 16:34:00",
         "2023/10/25 16:44:50"]  # 六項實際時間