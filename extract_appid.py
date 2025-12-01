# -------------------使用该脚本，从game_sessions.csv文件中提取所有不重复的AppID，并导出为unique_appids.csv-----------------------

import csv
import os


def extract_unique_appids(input_csv_path, output_csv_path):
    """
    解析 game_sessions.csv 文件，提取所有不重复的 AppID，并导出为 CSV 文件。

    :param input_csv_path: 输入的 CSV 文件路径 (game_sessions.csv)。
    :param output_csv_path: 导出的 CSV 文件路径 (unique_appids.csv)。
    """

    # 使用集合 (set) 来存储 AppID，集合自动处理去重
    unique_appids = set()
    app_id_column_name = 'AppID'

    try:
        # 读取 CSV 文件
        with open(input_csv_path, mode='r', newline='', encoding='utf-8') as infile:
            # 使用 DictReader 可以通过列名访问数据，更健壮
            reader = csv.DictReader(infile)

            # 检查 CSV 文件是否包含必要的列
            if app_id_column_name not in reader.fieldnames:
                print(f"错误：CSV 文件中未找到列名 '{app_id_column_name}'。请检查列名是否匹配。")
                print(f"文件中找到的列名: {reader.fieldnames}")
                return

            for row in reader:
                app_id = row.get(app_id_column_name)
                if app_id:  # 确保 AppID 不为空
                    unique_appids.add(app_id.strip())

    except FileNotFoundError:
        print(f"错误：未找到文件 {input_csv_path}。请确保文件路径正确。")
        return
    except Exception as e:
        print(f"读取 CSV 文件时发生错误: {e}")
        return

    # 导出到新的 CSV 文件
    try:
        # 将 set 转换为 list 并排序，以便导出时有序
        sorted_appids = sorted(list(unique_appids))

        with open(output_csv_path, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)

            # 写入表头
            writer.writerow(['AppID'])

            # 写入 AppID 列表
            for app_id in sorted_appids:
                writer.writerow([app_id])

        print(f"成功提取 {len(sorted_appids)} 个不重复的 AppID。")
        print(f"结果已导出到 {output_csv_path}")

    except Exception as e:
        print(f"写入 CSV 文件时发生错误: {e}")


# --- 脚本执行 ---
if __name__ == "__main__":
    INPUT_CSV = "game_sessions.csv"
    OUTPUT_CSV = "unique_appids.csv"

    print(f"开始处理文件: {INPUT_CSV}")
    extract_unique_appids(INPUT_CSV, OUTPUT_CSV)