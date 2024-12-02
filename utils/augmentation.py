import numpy as np
import geopandas as gpd
from shapely.geometry import Point
from sklearn.neighbors import KDTree

def generate_grid_points(x, y, radius, term):
    x_min, x_max = x - radius, x + radius
    y_min, y_max = y - radius, y + radius

    x_list = np.arange(x_min, x_max, term)
    y_list = np.arange(y_min, y_max, term)
    X, Y = np.meshgrid(x_list, y_list)
    points = [Point(x, y) for x, y in zip(X.ravel(), Y.ravel())]

    gdf = gpd.GeoDataFrame(geometry=points)
    gdf['distance'] = gdf.distance(Point(x, y))

    result = gdf[gdf['distance'] <= radius]

    result = np.array([[result.x, result.y] for result in result.geometry])

    return result

def idw_interpolation(dists, indices, neighbor_values, power):
    interpolated_values = []
    for i in range(len(dists)):
        weights = 1 / (dists[i] + 1e-10)**power
        interpolated_value = np.sum(weights * neighbor_values[indices[i]]) / np.sum(weights)
        interpolated_values.append(interpolated_value)
        
    return np.array(interpolated_values)

def select_points_by_value(points, values, num_point): 
    sorted_idx = np.argsort(values) 
    selected_points = points[sorted_idx][:num_point] 
    selected_values = values[sorted_idx][:num_point] 
    return selected_points, selected_values
