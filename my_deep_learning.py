import numpy as np
import pandas as pd
import sklearn as sk
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt

def example1:
    # creat classifier / regressor object -> construct임
    knn = KNeighborsClassifier(n_neighbors=3)

    # train to a training dataset 대부분의 학습함수는 .fit 임...
    knn.fit(x_train, y_train)

    # use it 대부분의 실행함수는 .predict 임...
    prediction = knn.predict(x_new)

    np.concatenate()

