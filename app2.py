from flask import Flask, render_template,request
#scientific computing library for saving, reading, and resizing images
import cv2
#for matrix math
import numpy as np
#for importing our keras model
import keras
#for regular expressions, saves time dealing with string data
import re
import numpy as np
#system level operations (like loading files)
import sys 
#for reading operating system data
import os
#from keras.models import load_model
#import tensorflow as tf
from PIL import Image
import imutils
from letters import send_json
from io import BytesIO
import base64
import tensorflow as tf


model = tf.keras.models.load_model('./model2.h5')
def stringToImage(base64_string):
    # img_color = cv2.cvtColor(np.array(Image.open(io.BytesIO(base64.b64decode(base64_string)))), cv2.COLOR_BGR2RGB)
    # cv2.imwrite('output.png',img_color)
    # print('#'*60)
    s = base64_string.decode('utf-8')
    s = s.split(',')[1]
    # print(base64_string)
    im = Image.open(BytesIO(base64.b64decode(s)))
    im.save("output.png")
    # print(type(base64_string))
    # with open("output.png", "wb") as fh:
    #     fh.write(base64.decodebytes(base64_string))

def decode_base64(data, altchars=b'+/'):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    print(type(data))
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'='* (4 - missing_padding)
    with open("output.png", "wb") as fh:
        fh.write(base64.b64decode(data, altchars))

def convertImage(imgData1):
	#imgstr = re.search(r'base64,(.*)',imgData1).group(1)
	#print(imgstr)
    print(type(imgData1))
    print(imgData1)
    with open('output.png','wb') as output:
        output.write(base64.b64decode((imgData1 + b'=' * (-len(imgData1) % 4))))
        #output.write(imgData1.decode('utf-8'))

app = Flask(__name__)

@app.route('/')
def home():
	#initModel()
	#render out pre-built HTML file right on the index page
    return render_template("landing.html")
@app.route('/learn')
def learn():
    letters = send_json()
	#initModel()
	#render out pre-built HTML file right on the index page
    return render_template("index.html",letters=letters)



@app.route('/test')
def tes():
	#initModel()
	#render out pre-built HTML file right on the index page
    letters = send_json()
    return render_template("index.html",letters=letters)

@app.route('/predict',methods=['GET','POST'])
def predict():
    #
    labelNames = "abcdefghijklmnopqrstuvwxyz".upper()
    letters = send_json()
    letters = {int(i):j for i,j in letters.items()}
    #whenever the predict method is called, we're going
    #to input the user drawn character as an image into the model
    #perform inference, and return the classification
    #get the raw data format of the image
    imgData = request.get_data()
    stringToImage(imgData)
    x = cv2.imread('output.png')
    
    #print(imgData)
    #encode it into a suitable format
    #convertImage(imgData)
    #print(imgData)
    #print ("debug")
    #read the image into memory

    #x = cv2.imread('output.png')
    

    #compute a bit-wise inversion so black becomes white and vice versa
    
    #x = np.invert(x)
    #cv2.imwrite('trial.png',x)
    #make it the right size
    #x = np.expand_dims(x,axis=-1)
    x = cv2.resize(x,(100,100))
    x = x >= 180
    x = x.astype("int16") * 255
    #x = cv2.merge([x,x,x])
    x = x.astype("float32") / 255.0
    x = np.expand_dims(x,axis=-1)
    cv2.imwrite('imge.png', x)
    #x = cv2.cvtColor(x, cv2.COLOR_GRAY2BGR)
    
    print(x.shape)
   # x = x[:,:,0]
    
    #x = x.reshape(x.shape[0],3,32,32)
    x = x.reshape(1, 100, 100, 3).astype('float32')
    #x  = x/255
    
    out = model.predict(x)
    prediction = np.argmax(out)
    preds = [labelNames[i] for i in np.argsort(out)[0][-3:]]
    print(preds)
    print(labelNames[prediction],out[0][-1])

    # letters = send_json()
    return labelNames[prediction]
    # return str(prediction[0])

#new_func()



if __name__ == "__main__":
	app.run(debug=True)