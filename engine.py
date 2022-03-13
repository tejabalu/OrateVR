import heartpy as hp
import numpy as np
import pandas as pd
import firebase_admin
import datetime
from firebase_admin import db
from scipy.signal import resample
import math
from mlengine import machine_learning

cred_obj = firebase_admin.credentials.Certificate('SAK.json')
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': 'https://nodemcutest-e668d-default-rtdb.firebaseio.com/'
})

ref = db.reference('/data_collection/path2test4/')
ref1 = db.reference('/data_collection/Engine/')

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
    
    resampled = resample(filtered, len(filtered)*10)
    new_sample_rate = sample_rate * 10
    print("new sample rate: ", new_sample_rate)
    
    stack = []
    try:
        wd, m = hp.process(resampled[-int(10*new_sample_rate):], sample_rate = new_sample_rate, 
                        high_precision=False, clean_rr=False)
        
        # print wd, m
        print(m["bpm"])
        print(type(m))
        stack = [m["breathingrate"], m["sdnn"], m["rmssd"], m["sdsd"], m["bpm"], m["pnn20"], m["pnn50"], m["sd1"], m["sd2"]]
        stack = [0 if math.isnan(x) else x for x in stack]
        print(stack)
        heart_rate = m["bpm"]
        heart_rate_update(heart_rate)
        stress_condition = stress_condition_update([stack])
    except:
        print("Error HR")
        stress_condition = "Stress levels not found"
    
    return [stack, stress_condition]

def stress_condition_update(stack):
    stress_condition = machine_learning(stack)
    try:
        ref1.child(path='Stress Condition').set(stress_condition)
        print("Stress Condition Updated")
    except:
        ref1.child(path='Stress Condition').set("Stress levels not found")
        print("Stress Condition not updated")
    
    return stress_condition

def heart_rate_update(bpm):
    try:
        ref1.child(path='Heart Rate').set(bpm)
        print("Heart Rate Updated")
    except:
        ref1.child(path='Heart Rate').set("Heart Rate not found")
        print("Heart rate not updated")