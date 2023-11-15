import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# 假设你的DataFrame是df，包含TIME和NO2列
# 请替换下面的数据为你实际的数据
data = {'TIME': ['10:00:00', '10:30:00', '11:00:00', '11:30:00', '12:00:00', '12:30:00', '13:00:00', '13:30:00', '14:00:00', '14:30:00'],
        'NO2': [15, 20, 30, 40, 50, 60, 70, 80, 90, 100]}
df = pd.DataFrame(data)

# 将 'TIME' 列转换为日期时间对象，只包含时分秒
df['TIME'] = pd.to_datetime(df['TIME'], format='%H:%M:%S').dt.time

# 将 'TIME' 列转换为秒数
df['TIME'] = df['TIME'].apply(lambda x: x.hour * 3600 + x.minute * 60 + x.second)

# 存储结果的列表
regression_results = []

# 迭代计算线性回归参数和R平方值
for i in range(len(df) - 1):
    window_data = df['NO2'].iloc[i:i + 2].values.reshape(-1, 1)
    window_time = np.arange(2).reshape(-1, 1)

    model = LinearRegression()
    model.fit(window_time, window_data)

    a, b = model.coef_[0][0], model.intercept_[0]

    predicted_values = model.predict(window_time)
    r2 = r2_score(window_data, predicted_values)

    # 存储结果
    regression_results.append({'start_time': df['TIME'].iloc[i], 'a': a, 'b': b, 'r2': r2})

# 将结果转换为DataFrame
result_df = pd.DataFrame(regression_results)

# 打印结果
print(result_df)
