import numpy as np
from PIL import Image
import base64
import re
from io import BytesIO


def get_image(image_b64):
    imgstr = re.search(r'base64,(.*)', image_b64).group(1)
    image_bytes = BytesIO(base64.b64decode(imgstr))
    im = Image.open(image_bytes).convert('L')
    im.thumbnail((128,128), Image.NEAREST)
    arr = np.array(im)
    print(arr.shape) # 128,128
    return arr

def predict(image_b64,model):
    img = get_image(image_b64)
    img = img.reshape((1,128,128,1))
    img = img/255
    result = model.predict(img)
    return result
    