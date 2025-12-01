# SDU_Visualization
The raw data (game log files) is processed as follows:
（将"你的steam_download目录\logs\gameprocess_log.txt"复制到与脚本同目录下） --> 
log2csv.py --> extract_appid.py --> （自行准备包含“AppID-游戏名称”对应关系的csv文件） --> 
id2game.py --> game_sessions_named.csv
