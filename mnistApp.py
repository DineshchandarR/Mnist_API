#import packages
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
from keras.preprocessing import image
from keras.models import model_from_json
import flask
from PIL import Image
from flask import Flask, request, json, jsonify
import io
import os

#Loading the model
def modelAct():
    json_file = open('mnist.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    # load weights into new model
    model.load_weights("mnist.h5")
    print('model loaded successfully')
    return model

#Transform Loading
def transform_image(pillow_image):
    data = np.asarray(pillow_image)
    data = data / 255.0
    data = data[np.newaxis, ..., np.newaxis]
    # --> [1, x, y, 1]
    data = tf.image.resize(data, [28, 28])
    return data

#Predict
def predict (img_data):
    model = modelAct()
    prediction = None
    result = None
    result = model.predict(img_data)
    print(np.max(result))
    print(result[0])
    for i in range(10):
        if result[0][i] == np.max(result):
            prediction = i
            
    return prediction

#Application
app = Flask(__name__)


@app.route ("/", methods = ["GET","POST"])
def index():
    welcomeMsg = "Welcome to MNIST digit analysis, by DINESHCHANDAR RAVICHANDRAN \n contact me @: dravich@g.g.clemson.edu\n"
    if request.method == "POST":
        file = request.files['file']
        if file is None or file.filename == "":
            return jsonify ({"error": "No input found!"})
        else:
           
            try:
                image_bytes = file.read()
                pillow_img = Image.open(io.BytesIO(image_bytes)).convert('L')
                tensor = transform_image(pillow_img)
                prediction = predict(tensor)
                result = {"Prediction": int(prediction)}
                print(result)
                return jsonify (welcomeMsg,result)
            except Exception as e:
                return jsonify (welcomeMsg,{"error":str(e)})
    else:
        return "Health check: OK"


if __name__ == "__main__":
 port = int(os.environ.get('PORT', 8000))
 app.run(debug=True, host='0.0.0.0', port=port)