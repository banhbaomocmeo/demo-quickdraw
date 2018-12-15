import numpy as np
import matplotlib.pyplot as plt
# from keras.models import load_model
# from keras.applications.mobilenet import preprocess_input
# from keras import backend as K

# ... code
# a= np.random.randint(255, size=(1,128,128,1))
# a = preprocess_input(a.astype(np.float32))


# model = load_model('accuracy_0.8402352932.hdf5')
# b=model.predict(a)
# K.clear_session()
# print(b)

a = np.load('img.npy')
plt.imshow(a, cmap='gray')
plt.show()