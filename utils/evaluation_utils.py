from sklearn.metrics import mean_absolute_error, mean_squared_error, root_mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

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
