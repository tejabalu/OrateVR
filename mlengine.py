from keras.models import load_model
from engine import export_heartrate

model = load_model('model.h5')
def machine_learning():
    stack = export_heartrate()
    return model.predict([[0,0,0,0,0,0,0,0,0]])
