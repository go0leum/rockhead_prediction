import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import utm # 좌표계 변환

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