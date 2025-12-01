#----------- 该脚本用于将game_sessions.csv中的AppID列转换为对应的游戏名称 -----------

import pandas as pd

# 读取游戏游玩记录
sessions = pd.read_csv('game_sessions.csv')

# 读取 AppID → 游戏名称映射
mapping = pd.read_csv('id-game.csv')

# 根据你的文件实际内容调整列名
mapping.columns = ['AppID', '游戏名称']

# 合并两个表
merged = sessions.merge(mapping, how='left', on='AppID')

# 删除没有匹配到游戏名称的行
merged = merged.dropna(subset=['游戏名称'])

# 删除原 AppID 列（如果想保留，可注释掉）
merged = merged.drop(columns=['AppID'])

# 调整列顺序
merged = merged[['开始时间', '结束时间', '游戏名称']]

# 输出为新的 CSV 文件
merged.to_csv('game_sessions_named.csv', index=False, encoding='utf-8-sig')

print("处理完成！输出文件：game_sessions_named.csv")
