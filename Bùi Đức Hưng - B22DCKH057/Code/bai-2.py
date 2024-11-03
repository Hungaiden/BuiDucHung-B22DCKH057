import pandas as pd
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
from collections import Counter
import os
import time
def get_top3_player(df, column_to_analyze):
    # Top 3 cao nhat
    with open("Top3NguoiChiSoCaoNhat.txt", "w", encoding="utf-8") as file:
        for column in columns_to_analyze:
            file.write(f"\nTop 3 cầu thủ cao nhất cho chỉ số '{column}':\n")
            top_highest = df.nlargest(3, column)[['Player Name', 'Team', column]]
            file.write(tabulate(top_highest, headers='keys', tablefmt='fancy_grid') + "\n")
        
        print("----Đã ghi kết quả Top 3 cầu thủ cao nhất vào file Top3NguoiChiSoCaoNhat.txt-----")

    # Top 3 thấp nhất
    with open("Top3NguoiChiSoThapNhat.txt", "w", encoding="utf-8") as file:
        for column in columns_to_analyze:
            file.write(f"\nTop 3 cầu thủ thấp nhất cho chỉ số '{column}':\n")
            top_lowest = df.nsmallest(3, column)[['Player Name', 'Team', column]]
            file.write(tabulate(top_lowest, headers='keys', tablefmt='fancy_grid') + "\n")

        print("----Đã ghi kết quả Top 3 cầu thủ thấp nhất vào file Top3NguoiChiSoThapNhat.txt----")

   
def calculate_statistics(df, columns_to_analyze):
    # Tính các thống kê trung vị, trung bình, độ lệch chuẩn cho toàn giải và từng đội

    # Tính toán toàn giải
    overall_stats = pd.DataFrame({
        'Team': ['All'],
        **{f"{stat.capitalize()} of {col}": getattr(df[col], stat)().round(2) for col in columns_to_analyze for stat in ['median', 'mean', 'std']}
    })
    
    # Tính toán cho từng đội
    team_stats = df.groupby('Team')[columns_to_analyze].agg(['median', 'mean', 'std']).round(2).reset_index()
    team_stats.columns = ['Team'] + [f"{stat.capitalize()} of {col}" for col in columns_to_analyze for stat in ['median', 'mean', 'std']]

    # Kết hợp và lưu file CSV
    final_stats = pd.concat([overall_stats, team_stats], ignore_index=True)
    final_stats.to_csv('results2.csv', index=False, encoding='utf-8-sig')
    print("<<<<<<<<Đã xuất kết quả ra file results2.csv>>>>>>>>")

def plot_histograms(df, column_to_analyze):
    # Tên thư mục để lưu trữ các biểu đồ toàn giải
    output_folder_1 = "histograms_all"

    # Tạo thư mục nếu chưa tồn tại
    if not os.path.exists(output_folder_1):
        os.makedirs(output_folder_1)

    # Vẽ histogram cho toàn giải
    for col in columns_to_analyze:
        plt.figure(figsize=(8, 6))
        sns.histplot(df[col], bins=20, kde=True, color='blue')
        
        plt.title(f'Histogram of {col} - Toàn Giải')
        plt.xlabel(col)
        plt.ylabel('Số lượng cầu thủ (Người)')
        
        plt.grid(True, linestyle='--', alpha=0.5)
        # Lưu biểu đồ vào thư mục "histograms_all"
        
        plt.savefig(os.path.join(output_folder_1, f"{df.columns.get_loc(col)}.png"))
        plt.close()

    print("Đã vẽ xong biểu đồ cho toàn giải")

    # Tên thư mục để lưu trữ các biểu đồ các đội
    output_folder_2 = "histograms_teams"

    # Tạo thư mục nếu chưa tồn tại
    if not os.path.exists(output_folder_2):
        os.makedirs(output_folder_2)

    # Vẽ histogram cho từng đội
    teams = df['Team'].unique()
    for team in teams:
        # Tên thư mục của đội
        team_folder = os.path.join(output_folder_2, team)
        # Tạo thư mục nếu chưa tồn tại
        if not os.path.exists(team_folder):
            os.makedirs(team_folder)

        team_data = df[df['Team'] == team]
        
        for col in columns_to_analyze:
            plt.figure(figsize=(8, 6))
            sns.histplot(team_data[col], bins=20, kde=True, color='green')
            plt.title(f'Histogram of {col} - {team}')
            plt.xlabel(col)
            plt.ylabel('Số lượng cầu thủ (Người)')
            plt.grid(True, linestyle='--', alpha=0.5)
            # Lưu biểu đồ vào thư mục của đội
            plt.savefig(os.path.join(team_folder, f"{df.columns.get_loc(col)}.png"))
            plt.close()
        
        print(f"Đã hoàn thành biểu đồ cho đội {team}")
        time.sleep(3)
    
    print("----Hoàn thành vẽ biểu đồ cho toàn giải và từng đội----")



def identify_best_team(df, columns_to_analyze):
    # Chuyển các cột chỉ số thành dạng số, thay thế các giá trị không hợp lệ bằng NaN
    metric_columns = df.columns[8:]
    df[metric_columns] = df[metric_columns].apply(pd.to_numeric, errors='coerce')

    # Tính trung bình các chỉ số theo từng đội
    team_averages = df.groupby('Team')[metric_columns].mean()

    # Tạo danh sách lưu đội có giá trị cao nhất cho từng chỉ số
    results = [
        [col, team_averages[col].idxmax(), team_averages[col].max()]
        for col in metric_columns
    ]

    # In bảng kết quả đội có chỉ số cao nhất cho từng chỉ số
    print("Đội có giá trị cao nhất cho từng chỉ số:")
    print(tabulate(results, headers=["Chỉ số", "Team", "Giá trị"], tablefmt="grid"))

    # Đếm số lần mỗi đội có giá trị cao nhất ở các chỉ số
    team_frequencies = Counter([result[1] for result in results])

    # Chuyển kết quả đếm tần suất thành dạng bảng, sắp xếp giảm dần theo số lần
    frequency_table = sorted(
        [[team, freq] for team, freq in team_frequencies.items()],
        key=lambda x: x[1],
        reverse=True
    )

    # In bảng tần suất của từng đội
    print("\nTần suất các đội bóng xuất hiện ở vị trí dẫn đầu:")
    print(tabulate(frequency_table, headers=["Team", "Số lần"], tablefmt="grid"))

    # Xác định đội có phong độ tốt nhất dựa trên tần suất cao nhất
    best_team = frequency_table[0][0]
    best_team_count = frequency_table[0][1]
    print(f"Đội có phong độ tốt nhất là: {best_team} với số lần xuất hiện ở vị trí dẫn đầu: {best_team_count}")
    print("=> Đây là đội có phong độ tốt nhất giải Ngoại Hạng Anh mùa 2023-2024")

    
if __name__ == "__main__":
    df = pd.read_csv("results.csv")

    columns_to_analyze = df.columns[4:]  # Chỉ chọn các cột chỉ số từ cột "Non-Penalty Goals" trở đi

    # chuyển thành NaN
    df[columns_to_analyze] = df[columns_to_analyze].apply(pd.to_numeric, errors='coerce')
    
    
    get_top3_player(df, columns_to_analyze)     
    calculate_statistics(df, columns_to_analyze)
    plot_histograms(df, columns_to_analyze)
    identify_best_team(df, columns_to_analyze)
        
    

