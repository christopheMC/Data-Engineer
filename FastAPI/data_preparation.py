import pandas as pd
from donnees import Features


sex_dict = {"M": 1, "F": 0}
source_dict = {'SEO':0,'Ads':1,'Direct':2}
browser_dict = {'Safari':0,'IE':1,'Chrome':2,'Opera':3,'FireFox':4}

def prepare_data(data: Features):
    df = pd.DataFrame([data.dict()])
    df["sex"] = df["sex"].map(sex_dict)
    df['source'] = df['source'].map(source_dict)
    df['browser'] = df['browser'].map(browser_dict)
    df['purchase_time'] = pd.to_datetime(df.purchase_time)
    df['purchase_month'] = df.purchase_time.dt.month
    df['signup_time'] = pd.to_datetime(df.signup_time)
    df['diff_time'] = df['purchase_time'] - df['signup_time']
    df['diff_day'] = df.diff_time.dt.days
    df['diff_hour'] = df.diff_time.dt.components['hours']
    df['diff_minute'] = df.diff_time.dt.components['minutes']
    df['diff_second'] = df.diff_time.dt.components['seconds']
    df = df.drop(['device_id', 'signup_time', 'purchase_time', 'diff_time','user_id'], axis=1)
    return df