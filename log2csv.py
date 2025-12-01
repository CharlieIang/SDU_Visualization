# --------------使用该脚本，解析本地Steam游戏日志文件，提取游戏会话记录，并导出为game_sessions.csv----------------

import re
import csv
from datetime import datetime
import os


def parse_steam_game_log(log_file_path, output_csv_path):
    """
    解析 Steam 游戏日志文件，提取游戏会话记录，并导出为 CSV 文件。

    :param log_file_path: 游戏日志文件的路径 (gameprocess_log.txt)。
    :param output_csv_path: 导出 CSV 文件的路径 (game_sessions.csv)。
    """

    # 正则表达式用于匹配游戏开始和结束的行
    # 开始：[YYYY-MM-DD HH:MM:SS] AppID XXXXXXX adding PID...
    start_pattern = re.compile(r"^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] AppID (\d+) adding PID")

    # 结束：[YYYY-MM-DD HH:MM:SS] Remove XXXXXXX from running list
    end_pattern = re.compile(r"^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] Remove (\d+) from running list")

    # 存储当前正在运行的游戏会话：{AppID: 开始时间戳}
    active_sessions = {}

    # 存储完整的游戏会话记录：[(开始时间, 结束时间, AppID), ...]
    completed_sessions = []

    try:
        with open(log_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # 尝试匹配游戏开始
                start_match = start_pattern.match(line)
                if start_match:
                    timestamp_str, app_id = start_match.groups()
                    # 仅记录首次启动的 PID，作为会话的开始时间
                    if app_id not in active_sessions:
                        active_sessions[app_id] = timestamp_str
                    continue

                # 尝试匹配游戏结束
                end_match = end_pattern.match(line)
                if end_match:
                    timestamp_str, app_id = end_match.groups()

                    if app_id in active_sessions:
                        start_time_str = active_sessions.pop(app_id)
                        # 记录完整的会话
                        completed_sessions.append({
                            '开始时间': start_time_str,
                            '结束时间': timestamp_str,
                            'AppID': app_id
                        })
                    continue

    except FileNotFoundError:
        print(f"错误：未找到文件 {log_file_path}。请确保文件路径正确。")
        return
    except Exception as e:
        print(f"读取或解析文件时发生错误: {e}")
        # 即使发生错误，也尝试将已解析的数据写入 CSV
        pass

    # 处理日志末尾仍处于“运行中”状态的会话
    for app_id, start_time_str in active_sessions.items():
        completed_sessions.append({
            '开始时间': start_time_str,
            '结束时间': '未结束 (Not Ended)',
            'AppID': app_id
        })

    # 导出到 CSV
    fieldnames = ['开始时间', '结束时间', 'AppID']
    try:
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(completed_sessions)

        print(f"成功将 {len(completed_sessions)} 条游戏会话记录导出到 {output_csv_path}")
        print("注意：如果 '结束时间' 为 '未结束 (Not Ended)'，则表示日志文件在游戏退出前结束。")

    except Exception as e:
        print(f"写入 CSV 文件时发生错误: {e}")


# --- 脚本执行 ---
if __name__ == "__main__":
    LOG_FILE = "gameprocess_log.txt"
    OUTPUT_CSV = "game_sessions.csv"

    print(f"开始解析日志文件: {LOG_FILE}")
    parse_steam_game_log(LOG_FILE, OUTPUT_CSV)