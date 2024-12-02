import numpy as np
import geopandas as gpd
import libpysal as ps
from pysal.explore import esda
from tqdm import tqdm

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

def connected_distance(min_distance, max_distance, term, data):
    disconnected_flag = 0
    island_flag = 0

    data_copy = data[['x','y','depth_start']]

    # GeoDataFrame으로 변환
    gdf = gpd.GeoDataFrame(data_copy, geometry=gpd.points_from_xy(data_copy.x, data_copy.y))

    y = gdf['depth_start']  # 분석할 변수명을 지정

    for distance in tqdm(range(min_distance, max_distance, term)):
        # 고정 거리 밴드 가중치 행렬 
        w = ps.weights.DistanceBand.from_dataframe(gdf, threshold=distance, silence_warnings = True)
        
        island_count = len(w.islands)
        min_neighbors = w.min_neighbors
    
        if island_count == 0 and island_flag == 0:
            island_flag = 1
            island_distance = distance
            
        if min_neighbors > 1 and disconnected_flag == 0:
            disconnected_flag = 1
            disconnected_distance = distance
            break

    if island_flag == 1:
        print(f"not island minimum distance band: {island_distance}m")
    
    if disconnected_flag == 1:
        print(f"all connected minimum distance band: {disconnected_distance}m")

    if island_flag == 0 and disconnected_flag == 0:
        print(f"There is no minimum distance in distance_range [{min_distance}, {max_distance}, {term}]")
        return None

    return disconnected_distance


    
def anseline_moran_I(distance, data):
    data_copy = data[['x','y','depth_start']]

    # GeoDataFrame으로 변환
    gdf = gpd.GeoDataFrame(data_copy, geometry=gpd.points_from_xy(data_copy.x, data_copy.y))

    y = gdf['depth_start']  # 분석할 변수명을 지정

    w = ps.weights.DistanceBand.from_dataframe(gdf, threshold=distance, silence_warnings = True)
    
    lisa = esda.Moran_Local(y, w, permutations=9999)

    neighbors_count = [len(neighbors) for neighbors in w.neighbors.values()]
    data['neighbors'] = neighbors_count
    data['moran_I'] = lisa.Is
    data['p-value'] = lisa.p_sim
    data['z-score'] = lisa.z_sim
    data['cotype'] = lisa.q

    return data

