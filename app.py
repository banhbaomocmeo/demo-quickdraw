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

print("load_model")
keras.backend.clear_session()
model = load_model('accuracy_0.8402352932.hdf5')
global graph
graph = tf.get_default_graph()

le = LabelEncoder()
le.classes_ = np.load("le_classes.npy")

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
    img = img.reshape((1,128,128,1)) / 255
    with graph.as_default():
        result = model.predict(img)[0]
        result_arg = np.argsort(result)[::-1][:3]
        acc  = result[result_arg]
    print(result)
    result_label = le.inverse_transform(result_arg)

    return jsonify({"label": list(result_label), "score": [3,2,1]})

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
