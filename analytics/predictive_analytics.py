from sklearn.linear_model import LinearRegression
import numpy as np

def predict_future_metrics(metrics):
    model = LinearRegression()
    X = np.array(range(len(metrics))).reshape(-1, 1)
    y = np.array(metrics).reshape(-1, 1)
    model.fit(X, y)
    prediction = model.predict([[len(metrics) + 1]])
    return prediction[0][0] 