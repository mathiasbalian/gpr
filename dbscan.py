import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from scipy.spatial.distance import pdist
import warnings
warnings.filterwarnings("ignore")

data = pd.read_csv("gpr_simulation_data.csv")

fig = plt.figure(figsize=(12, 7))

ax1 = fig.add_subplot(121, projection='3d')
ax1.scatter(
    data['longitude'], data['latitude'], data['depth'],
    c=data['detected'], cmap='bwr', s=50, label='Detected'
)
ax1.set_title("Initial Data")
ax1.set_xlabel("Longitude")
ax1.set_ylabel("Latitude")
ax1.set_zlabel("Depth")
ax1.legend()

filtered_data = data[data['detected'] == 1]
X = filtered_data[['latitude', 'longitude', 'depth']].dropna()

dbscan = DBSCAN(eps=1, min_samples=2)
labels = dbscan.fit_predict(X)

filtered_data['cluster'] = labels

cluster_stats = []
unique_labels = np.unique(labels)

for cluster_id in unique_labels:
    if cluster_id == -1:
        continue

    cluster_points = filtered_data[filtered_data['cluster'] == cluster_id][['latitude', 'longitude', 'depth']].values

    center = cluster_points.mean(axis=0)

    if len(cluster_points) > 1:
        distances = pdist(cluster_points)
        diameter = distances.max()
    else:
        diameter = 0

    cluster_stats.append({
        'cluster': cluster_id,
        'center_latitude': center[0],
        'center_longitude': center[1],
        'center_depth': center[2],
        'diameter': diameter
    })

cluster_stats_df = pd.DataFrame(cluster_stats)
print("Cluster Predictions:")
print(cluster_stats_df)

ax2 = fig.add_subplot(122, projection='3d')

colormap = plt.get_cmap('tab10')
colors = [colormap(i) for i in range(len(unique_labels))]

for label, color in zip(unique_labels, colors):
    if label == -1:
        cluster_points = filtered_data[filtered_data['cluster'] == label]
        ax2.scatter(
            cluster_points['longitude'], cluster_points['latitude'], cluster_points['depth'],
            c='gray', label="Noise", s=50, alpha=0.6
        )
    else:
        cluster_points = filtered_data[filtered_data['cluster'] == label]
        ax2.scatter(
            cluster_points['longitude'], cluster_points['latitude'], cluster_points['depth'],
            color=color, label=f"Cluster {label}", s=50, alpha=0.8
        )

        cluster_center = cluster_points[['latitude', 'longitude', 'depth']].mean(axis=0)
        ax2.scatter(
            cluster_center[1], cluster_center[0], cluster_center[2],
            c='black', marker='x', s=100, label=f"Center {label}"
        )

ax2.set_title("DBSCAN Clustering Results")
ax2.set_xlabel("Longitude")
ax2.set_ylabel("Latitude")
ax2.set_zlabel("Depth")
ax2.legend()

plt.tight_layout()
plt.show()
