from sklearn.metrics import mean_absolute_error, mean_squared_error, root_mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import utm # 좌표계 변환

def evaluation(y_true, y_pred, n, k):
    
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = root_mean_squared_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    adjusted_r2 = (1-r2)*(n-1)/(n-k-1)

    return mae, mse, rmse, r2, adjusted_r2

def barplot(data, x_col, y_col, figure_name, hue=None):
    plt.figure(figsize=(10, 6))
    sns.barplot(x=data[x_col], y=data[y_col], data=data, hue=hue)
    plt.title(figure_name)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.show()

def boxplot_2(data, x_col, y_col, figure_name):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=x_col, y=y_col, data=data)
    plt.title(figure_name)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.show()

def distribution_plot(data, x_col, y_col, figure_name):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=x_col, y=y_col, data=data)
    plt.title(figure_name)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.show()

def surface_3d(data, x_col, y_col, z_col):
    fig = go.Figure(data=[go.Surface(z=data[z_col], x=data[x_col], y=data[y_col])])
    fig.update_layout(
        title='3d bedrock start depth',
        autosize=False,
        width=1000,
        height=800,
        margin=dict(l=65, r=50, b=65, t=90)
    )

    fig.show()

def contour_plot(data, x_col, y_col, z_col):

    fig = go.Figure(data=go.Contour(
        z= utm.to_latlon(data[z_col]), x=utm.to_latlon(data[x_col]), y=utm.to_latlon(data[y_col]),
        colorscale='Viridis',
        contours=dict(
            start= -1,
            end= 1,
            size= 0.2
        )
    ))

    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_center=dict(lat=37.5665, lon=126.9780),  # 서울 중심 좌표
        mapbox_zoom=10
    )

    fig.show()