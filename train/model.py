from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import compute_class_weight
from sklearn.metrics import f1_score, classification_report, confusion_matrix
from sklearn.metrics import make_scorer
import pandas as pd
import numpy as np
import pickle


df = pd.read_csv('fraud.csv')
df = df.drop(['device_id','user_id'], axis=1)
df.sex = df.sex.replace(['M','F'],[1,0])
df.source = df.source.replace(['SEO','Ads','Direct'],[0,1,2])
df.browser = df.browser.replace(['Safari','IE','Chrome','Opera','FireFox'],[0,1,2,3,4])
df['purchase_time'] = pd.to_datetime(df.purchase_time)
df['signup_time'] = pd.to_datetime(df.signup_time)
df['diff_time'] = df['purchase_time'] - df['signup_time']
df['purchase_month'] = df.purchase_time.dt.month
df['diff_day'] = df.diff_time.dt.days
df['diff_hour'] = df.diff_time.dt.components['hours']
df['diff_minute'] = df.diff_time.dt.components['minutes']
df['diff_second'] = df.diff_time.dt.components['seconds']
df = df.sort_values(by='purchase_month')
data = df.drop(['is_fraud', 'signup_time', 'purchase_time', 'diff_time'], axis=1)
target = df.is_fraud

X_train, X_test, y_train, y_test = train_test_split(
    data, target, test_size=0.2, random_state=42
)

class_weights = compute_class_weight("balanced", classes=y_train.unique(), y=y_train)
class_weights = {i: class_weights[i] for i in range(len(class_weights))}

rfc = RandomForestClassifier()

def score(y_true, y_pred):
    class_weights = compute_class_weight(
        "balanced", classes=y_train.unique(), y=y_train
    )
    class_weights = {i: class_weights[i] for i in range(len(class_weights))}
    return f1_score(y_true, y_pred, sample_weight=y_true.map(class_weights))


my_scorer = make_scorer(score, needs_proba=False)

param_grid = {
    "max_depth": range(1, 5),
    "min_samples_split": range(2, 5),
    "n_estimators": range(10, 200, 10),
    "criterion": ['gini', 'entropy']
}

#RANDOM
random_rfc = RandomizedSearchCV(rfc, param_grid, scoring=my_scorer)
search = random_rfc.fit(X_train, y_train, sample_weight=y_train.map(class_weights))

print(search.best_params_)
print(search.best_score_)

best_estimator = search.best_estimator_

y_pred_train = best_estimator.predict(X_train)
y_pred_test = best_estimator.predict(X_test)

print("\n#### Train : ")

print(classification_report(y_train, y_pred_train))
print(confusion_matrix(y_train, y_pred_train))
print("F1 Score : ", f1_score(y_train, y_pred_train))


print("\n#### Test : ")

print(classification_report(y_test, y_pred_test))
print(confusion_matrix(y_test, y_pred_test))
print("F1 Score : ", f1_score(y_test, y_pred_test))



with open("./data/model.pkl", "wb") as f:
    pickle.dump(best_estimator, f)

with open("./data/scores.txt", "w") as f:
    f.write("# Train :\n")

    f.write(f"F1 Score : {f1_score(y_train, y_pred_train)}\n")
    f.write(f"Confusion Matrix :\n{str(confusion_matrix(y_train, y_pred_train))}")

    f.write("\n\n# Test :\n")

    f.write(f"F1 Score : {f1_score(y_test, y_pred_test)}\n")
    f.write(f"Confusion Matrix :\n{str(confusion_matrix(y_test, y_pred_test))}")



