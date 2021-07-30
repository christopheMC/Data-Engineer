from sklearn.model_selection import train_test_split, RandomizedSearchCV
from imblearn.combine import SMOTETomek
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import numpy as np

def prepare_model():
        df = pd.read_csv('fraud.csv', index_col = 'user_id')
        df.sex = df.sex.replace(['M','F'],[1,0])
        df['purchase_time'] = pd.to_datetime(df.purchase_time)
        df['purchase_month'] = df.purchase_time.dt.month
        df['signup_time'] = pd.to_datetime(df.signup_time)
        df['diff_time'] = df['purchase_time'] - df['signup_time']
        df['diff_day'] = df.diff_time.dt.days
        df['diff_hour'] = df.diff_time.dt.components['hours']
        df['diff_minute'] = df.diff_time.dt.components['minutes']
        df['diff_second'] = df.diff_time.dt.components['seconds']
        df = df.join(pd.get_dummies(df['source'], prefix='source'))
        df = df.join(pd.get_dummies(df['browser'], prefix='browser'))
        data = df.drop(['is_fraud', 'device_id', 'signup_time', 'purchase_time', 'source', 'browser', 'diff_time'], axis=1)
        tar = df.sort_values(by='purchase_month')
        target = tar.is_fraud
        data = data.sort_values(by='purchase_month')
        train_features = data[:int(data.shape[0]*0.8)]
        val_features = data[int(data.shape[0]*0.8):]
        train_target = target[:int(target.shape[0]*0.8)]
        val_target = target[int(target.shape[0]*0.8):]
        X_train, X_test, y_train, y_test = train_test_split(train_features, train_target, test_size=0.2)
        smt = SMOTETomek()
        X_train_res, y_train_res = smt.fit_resample(X_train, y_train)
        dt = DecisionTreeClassifier()
        parametres_dt = { 'criterion': ['gini', 'entropy'], 'max_depth': [2,4,6, 10, 50, 100], 'max_features': ['auto', 'sqrt', 'log2', None]}
        random_dt = RandomizedSearchCV(dt, parametres_dt)
        random_dt.fit(X_train_res, y_train_res)
        return random_dt

dt = prepare_model()
