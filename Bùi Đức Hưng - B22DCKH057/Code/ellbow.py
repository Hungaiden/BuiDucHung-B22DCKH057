from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('results.csv')
# Chọn các cột dữ liệu dạng số
numerical_data = data.select_dtypes(include=['float64', 'int64']).dropna(axis=1)

# Chuẩn hoá dữ liệu
scaler = StandardScaler()
data_scaled = scaler.fit_transform(numerical_data)

# Tính toán inertia cho các giá trị K khác nhau để áp dụng phương pháp Elbow
inertia = []
K_values = range(1, 11)

for k in K_values:
    kmeans = KMeans(n_clusters=k, random_state=0)
    kmeans.fit(data_scaled)
    inertia.append(kmeans.inertia_)

# Vẽ đồ thị Elbow
plt.figure(figsize=(10, 6))
plt.plot(K_values, inertia, marker='o', linestyle='-')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Inertia')
plt.title('Elbow Method for Optimal K')
plt.show()
