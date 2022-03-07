# import heartpy as hp
# import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import firebase_admin
import datetime
# import google.cloud
from firebase_admin import db

cred_obj = firebase_admin.credentials.Certificate('SAK.json')
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': 'https://nodemcutest-e668d-default-rtdb.firebaseio.com/'
})


def export_dataframe():
    ref = db.reference('/pulsetest/pushpulse')
    data = ref.get()

    df = pd.DataFrame(data)
    df.reset_index(drop=True, inplace=True)
    keys = np.array(list(df["data"][0].keys()))

    dfi = pd.DataFrame(columns=keys, dtype=np.float64)
    df['data'][0].values()

    for i in range(len(df["data"])):
        dfi = dfi.append((df["data"][i]), ignore_index=True)
    dfi["Ts"] = dfi["Ts"].apply(lambda x: x / 1000)
    dfi["formatted_time"] = dfi["Ts"].apply(lambda x: datetime.datetime.fromtimestamp(x))

    return dfi
