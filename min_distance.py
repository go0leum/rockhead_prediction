import pandas as pd
import geopandas as gpd
import libpysal as ps
from pysal.explore import esda

distances = range(100, 5000)  # 거리 밴드 설정 (단위: m)
morans_i = []
p_values = []
z_values = []

disconnedted_flag = 0

# CSV 파일 읽기
data = pd.read_csv("data/241007_rockhead_seoul.csv")

data = data[['x','y','depth_start']]

# GeoDataFrame으로 변환
gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.x, data.y))

y = gdf['depth_start']  # 분석할 변수명을 지정

for distance in distances:
    # 고정 거리 밴드 가중치 행렬 생성
    w = ps.weights.DistanceBand.from_dataframe(gdf, threshold=distance, silence_warnings = True)
    
    island_count = len(w.islands)
    min_neighbors = w.min_neighbors
    
    if min_neighbors > 2:
        disconnedted_flag += 1
    
    if island_count > 0 and disconnedted_flag > 1:
        continue
    else:
        lisa = esda.Moran_Local(y, w)
        morans_i = lisa.Is.mean()
        p_value = lisa.p_sim.mean()
        z_value = lisa.z_sim.mean()
    
        if disconnedted_flag == 1:
            print(f"all connected 최소 거리 밴드: {distance}m, Moran's I: {morans_i}, p-value: {p_value}, z-value: {z_value}")
        elif island_count == 1:
            print(f"not island 최소 거리 밴드: {distance}m, Moran's I: {morans_i}, p-value: {p_value}, z-value: {z_value}")