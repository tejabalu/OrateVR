from keras.models import load_model

model = load_model('model.h5')
def machine_learning(stack):
	stress_condition = "Stress levels not found"
	result = model.predict(stack)
	result = result.tolist()
	index = result.index(max(result))
	if index == 0:
		stress_condition = "Distracted"
	elif index == 1:
		stress_condition = "Stressed"
	elif index == 2:
		stress_condition = "Normal"
	return stress_condition
