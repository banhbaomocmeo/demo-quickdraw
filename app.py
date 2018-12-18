import os
import sys
import logging
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS

from serve import get_image
import tensorflow as tf
from keras.models import load_model
import keras
import numpy as np
from sklearn.preprocessing import LabelEncoder
from keras.applications.mobilenet import preprocess_input

print("load_model")
keras.backend.clear_session()
model = load_model('accuracy_0.8402352932.hdf5')
global graph
graph = tf.get_default_graph()

le = LabelEncoder()
classes_ = np.load("le_classes.npy")
classes_ = np.append(np.append(classes_[3:307], classes_[0:3]), classes_[307:])
le.classes_ = classes_

#tent-306 = 'The Mona Lisa'-2
#tennis racquet - 305 = 'The Great Wall of China'-302
#televison-304 = 'The Eiffel Tower'-0
#cat-66 = car-63
app = Flask(__name__)
CORS(app) # needed for cross-domain requests, allow everything by default

@app.route('/js/<path:filename>')
def serve_static_js(filename):
    return send_from_directory(os.path.join('.', 'static', 'js'), filename)

@app.route('/css/<path:filename>')
def serve_static_css(filename):
    return send_from_directory(os.path.join('.', 'static', 'css'), filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict_api():
    image_b64 = request.values['imageBase64']
    img = get_image(image_b64)
    np.save('img.npy', 255-img)
    img = 255 - img.reshape((1,128,128,1))
    img = preprocess_input(img.astype(np.float32))

    with graph.as_default():
        result = model.predict(img)[0]
        result_arg = np.argsort(result)[::-1][:3]
        
    acc  = result[result_arg]
    result_label = le.inverse_transform(result_arg)
    print(result_arg)
    return jsonify({"label": list(result_label), "score": list(acc.astype(np.float))})
    # return jsonify({"label": ["a","b","c"], "score": list(np.ones(3))})

# HTTP Errors handlers
@app.errorhandler(404)
def url_error(e):
    return """
    Wrong URL!
    <pre>{}</pre>""".format(e), 404


@app.errorhandler(500)
def server_error(e):
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally.
    app.run(host='localhost', debug=True, use_reloader=False)
