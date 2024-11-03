from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd
from tqdm import tqdm

# Khởi tạo các tùy chọn cho Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=chrome_options)

# URL
base_url = "https://www.footballtransfers.com/us/transfers/2023-2024-season-soccer-transfers"  # ví dụ URL


# Các danh sách lưu dữ liệu
name_players = []
from_teams = []
to_teams = []
date_transfers = []
transfer_prices = []

# Hàm để lấy dữ liệu từ trang hiện tại
def scrape_data():
    # Lấy tất cả các hàng trong bảng
    rows = driver.find_elements(By.XPATH, '//*[@id="player-table-body"]/tr')
    for row in rows:
        
        player = row.find_element(By.XPATH, './td[2]/div/div[2]')
        name_players.append(player.text)
        
        from_team = row.find_element(By.XPATH, './td[3]/div/div[1]/a')
        from_teams.append(from_team.get_attribute("title"))
        
        to_team = row.find_elements(By.XPATH, './td[4]/div/div[1]/a')
        to_team_name = ""
        
        # Kiểm tra từng phần tử để lấy tên đội bóng mới
        for team in to_team:
            if team.text:
                to_team_name = team.text  # lấy tên đầu tiên không rỗng
                break
        
        to_teams.append(to_team_name)
        
        date = row.find_element(By.XPATH, './td[3]')
        date_transfers.append(date.text)
        
        price = row.find_element(By.XPATH, './td[4]/span')
        transfer_prices.append(price.text)

# Sử dụng tqdm để hiển thị tiến độ
with tqdm(total=10, desc="Đang cào dữ liệu từ các trang", unit="trang") as pbar:
    for page_number in range(1, 11):
        
        url = f"{base_url}/{page_number}"
        driver.get(url)
        
        # Đợi cho đến khi phần tử bảng đã tải
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "player-table-body")))
        
        scrape_data()
        pbar.update(1)

# In dạng dataframe
data = {
    "Name": name_players,
    "From": from_teams,
    "To": to_teams,
    "Date": date_transfers,
    "Price": transfer_prices
}

df = pd.DataFrame(data)


# Lưu thành file csv
df.to_csv("football_transfers.csv", index=False)
