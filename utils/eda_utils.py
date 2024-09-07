import matplotlib.pyplot as plt
import seaborn as sns

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
        correlation_matrix = data[numeric_columns].drop(columns=[drop_column]).corr()

    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5)
    plt.title(figure_name)
    plt.show()

def box_plot(data, x_col, y_col, figure_name):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=x_col, y=y_col, data=data)
    plt.title(figure_name)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.show()


def scatter_relation(data, x_col, y_col, s, figure_name, hue=None):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=data, x=x_col, y=y_col, hue=hue, s=s)
    plt.title(figure_name)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.show()

def pairplot(data, figure_name, drop_column=False):
    numeric_columns = data.select_dtypes(include=['int64', 'float64']).columns
    if drop_column:
        correlation_matrix = data[numeric_columns].drop(columns=[drop_column]).corr()
    plt.figure(figsize=(10, 10))
    sns.pairplot(data)
    plt.title(figure_name)
    plt.show()
