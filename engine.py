import heartpy as hp
import numpy as np
import pandas as pd
import firebase_admin
import datetime
from firebase_admin import db
from scipy.signal import resample

cred_obj = firebase_admin.credentials.Certificate('SAK.json')
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': 'https://nodemcutest-e668d-default-rtdb.firebaseio.com/'
})

ref = db.reference('/data_collection/path2test4/')

def export_dataframe():
    data = ref.get()
    
    fulllist = []
    for d in data:
        fulllist.extend(data[d])

    fulllist = [x for x in fulllist if isinstance(x, str)]
    fulllist = [x.split(" | ") for x in fulllist]
    
    df = pd.DataFrame(fulllist)
    df.columns = ['Time', 'PPG', 'GSR']
    # convert all values to int
    df.PPG = df.PPG.astype(int)
    df.GSR = df.GSR.astype(int)
    df.Time = df.Time.astype(int)
    df["Formatted Time"] = df["Time"].apply(lambda x: datetime.datetime.fromtimestamp(x))

    
    return df

def export_heartrate():
    data = ref.get()
    
    fulllist = []
    for d in data:
        fulllist.extend(data[d])

    fulllist = [x for x in fulllist if isinstance(x, str)]
    fulllist = [x.split(" | ") for x in fulllist]
    
    df = pd.DataFrame(fulllist)
    df.columns = ['Time', 'PPG', 'GSR']
    # convert all values to int
    df.PPG = df.PPG.astype(int)
    df.GSR = df.GSR.astype(int)
    df.Time = df.Time.astype(int)
    df["Formatted Time"] = df["Time"].apply(lambda x: datetime.datetime.fromtimestamp(x))
    
    timer = df["Formatted Time"]
    datah = df["PPG"]
    datah = datah.astype(int)
    timer = np.array(timer)
    timer = timer.astype(str)
    for i in range(len(timer)):
        timer[i] = timer[i][:-6]
    
    sample_rate = hp.get_samplerate_datetime(timer, timeformat='%Y-%m-%dT%H:%M:%S.%f')
    print(sample_rate)
    
    filtered = hp.filter_signal(datah, [0.7, 3.5], sample_rate=sample_rate, 
                            order=3, filtertype='bandpass')
    
    resampled = resample(filtered, len(filtered)*5)
    new_sample_rate = sample_rate * 5
    
    stack = []
    try:
        wd, m = hp.process(resampled[-int(10*new_sample_rate):], sample_rate = new_sample_rate, 
                        high_precision=True, clean_rr=True)
        
        # print wd, m
        for measure in m.keys():
            stack.append(m[measure])
            print(measure, m[measure])
    except:
        print("Error")
    
    return stack

def machine_learning():
    
    pass