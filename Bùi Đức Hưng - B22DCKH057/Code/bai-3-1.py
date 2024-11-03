import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt


def plot_kmeans(data, centroids, clusters, step):
        plt.figure(figsize=(8, 6))

        # Tạo màu sắc ngẫu nhiên cho các cụm
        colors = plt.colormaps['viridis'](np.linspace(0, 1, k))

        # Vẽ các điểm dữ liệu theo cụm
        for i in range(k):
            points = data[clusters == i]
            plt.scatter(points[:, 0], points[:, 1], s=50, color=colors[i], label=f'Cluster {i}')
        plt.scatter(centroids[i, 0], centroids[i, 1], s=200, color=colors[i], marker='X', edgecolor='k')


        plt.title('K-means Clustering of Football Players')
        plt.xlabel('PC1')
        plt.ylabel('PC2')
        plt.legend()
        plt.show()


if __name__ == "__main__":
    
    data = pd.read_csv('results.csv')
    data = data.select_dtypes(exclude=['object'])
    data = data.fillna(data.mean())

    # Chuẩn hóa dữ liệu
    scaler_standard = StandardScaler() # Khởi tạo
    data = pd.DataFrame(scaler_standard.fit_transform(data), columns=data.columns)

    # Áp dụng PCA giảm số chiều xuống 2
    pca = PCA(n_components=2)
    data = pca.fit_transform(data)
    data = pd.DataFrame(data, columns=['PC1', 'PC2'])

    # Số lượng cụm
    k = 4

    # Khởi tạo ngẫu nhiên các tâm cụm
    centroids = data.sample(n=k).values

    # Khởi tạo nhãn cho các điểm dữ liệu
    clusters = np.zeros(data.shape[0])

    epochs = 100
    for step in range(epochs):  # Giới hạn số bước lặp
        # Bước 1: Gán nhãn dựa trên khoảng cách đến các tâm cụm
        for i in range(len(data)):
            distances = np.linalg.norm(data.values[i] - centroids, axis=1)
            clusters[i] = np.argmin(distances)

        # Bước 2: Cập nhật các tâm cụm
        new_centroids = np.array([data.values[clusters == j].mean(axis=0) for j in range(k)])

        # Kiểm tra nếu các tâm cụm không thay đổi thì kết thúc
        if np.all(centroids == new_centroids):
             # Vẽ biểu đồ
            plot_kmeans(data.values, centroids, clusters, step)
            break

        centroids = new_centroids