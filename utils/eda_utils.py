import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import geopandas as gpd
import libpysal as ps
from pysal.explore import esda
from tqdm import tqdm

def distribution_histogram(data, x_col, figure_name, hue=None):
    plt.figure(figsize=(10, 6))
    sns.histplot(data, bins=30, x=x_col, kde=True, hue=hue)
    plt.title(figure_name)
    plt.xlabel(x_col)
    plt.ylabel('frequency')
    plt.show()

def count_historgram(data, column_name, figure_name):
    plt.figure(figsize=(10, 6))
    sns.countplot(x=column_name, data=data)
    plt.title(figure_name)
    plt.xlabel(column_name)
    plt.ylabel('count')
    plt.show()

def correlation_matrix(data, figure_name, drop_column=False):
    numeric_columns = data.select_dtypes(include=['int64', 'float64']).columns

    if drop_column:
        correlation_matrix = data[numeric_columns].drop(columns=drop_column).corr()
    else:
        correlation_matrix = data[numeric_columns].corr()

    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', vmin=-1, vmax=1, linewidths=0.5)
    plt.title(figure_name)
    plt.show()

def box_plot(data, x_col, y_col, figure_name):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=x_col, y=y_col, data=data)
    plt.title(figure_name)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.show()


def scatter_relation(data, x_col, y_col, s, figure_name, hue=None, hue_norm=None):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=data, x=x_col, y=y_col, hue=hue, s=s, hue_norm=hue_norm)
    plt.title(figure_name)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.show()

def pairplot(data, figure_name, drop_column=False):
    numeric_columns = data.select_dtypes(include=['int64', 'float64']).columns

    if drop_column:
        data = data[numeric_columns].drop(columns=drop_column)

    plt.figure(figsize=(10, 10))
    sns.pairplot(data)
    plt.title(figure_name)
    plt.show()

def remove_outlier(data, figure_name):
    Q1 = np.percentile(data[figure_name], 25, method='midpoint')
    Q3 = np.percentile(data[figure_name], 75, method='midpoint')

    IQR = Q3 - Q1
    upper = Q3+1.5*IQR
    lower = Q1-1.5*IQR

    upper_array = np.where(data[figure_name] >= upper)[0]
    lower_array = np.where(data[figure_name] <= lower)[0]

    outliers = data.loc[np.concatenate((upper_array, lower_array)).tolist()]

    return_data = data.drop(index=upper_array)
    return_data = return_data.drop(index=lower_array)

    return data, outliers

def prediction_plot(data, col1, col2, c):
    sc1 = plt.scatter(data[col1], data[col2], c=data[c], cmap='viridis', alpha=0.5)
    max_val = max(data[col1].max(), data[col2].max())
    
    plt.figure(figsize=(10, 10))
    plt.plot([0, max_val], [0, max_val], color='red', linestyle='--', label="y=x")
    plt.xlabel(col1)
    plt.ylabel(col2)
    plt.colorbar(sc1, label=c)  # 색상 막대 추가
    plt.grid(True)
    plt.show()
    
def min_distance(distance_range, data):

    disconnedted_flag = 0
    island_flag = 0

    data = data[['x','y','depth_start']]

    # GeoDataFrame으로 변환
    gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.x, data.y))

    y = gdf['depth_start']  # 분석할 변수명을 지정

    for distance in tqdm(distance_range):
        # 고정 거리 밴드 가중치 행렬 
        w = ps.weights.DistanceBand.from_dataframe(gdf, threshold=distance, silence_warnings = True)
        
        island_count = len(w.islands)
        min_neighbors = w.min_neighbors
        
        if island_count == 0 and island_flag == 0:
            island_flag = 1
            island_distance = distance
            lisa = esda.Moran_Local(y, w)
            island_morans_i = lisa.Is.mean()
            island_p_value = lisa.p_sim.mean()
            island_z_value = lisa.z_sim.mean()
            
        elif min_neighbors > 1 and disconnedted_flag == 0:
            disconnedted_flag = 1
            disconnected_distance = distance
            lisa = esda.Moran_Local(y, w)
            disconnected_morans_i = lisa.Is.mean()
            disconnected_island_p_value = lisa.p_sim.mean()
            disconnected_island_z_value = lisa.z_sim.mean()

    print(f"all connected 최소 거리 밴드: {disconnected_distance}m, Moran's I: {disconnected_morans_i}, p-value: {disconnected_island_p_value}, z-value: {disconnected_island_z_value}")
    print(f"not island 최소 거리 밴드: {island_distance}m, Moran's I: {island_morans_i}, p-value: {island_p_value}, z-value: {island_z_value}")

    return disconnected_distance