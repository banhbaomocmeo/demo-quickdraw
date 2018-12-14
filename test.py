import numpy as np
from keras.models import load_model

a=np.zeros((1,128,128,1))

model = load_model('accuracy_0.8402352932.hdf5')
b=model.predict(a)
print(b)