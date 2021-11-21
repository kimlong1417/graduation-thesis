1from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request

import numpy as np
import cv2
import base64

app = Flask(__name__)
# Apply Flask CORS
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
img = "D:\\Download\\SGU-LOGO.png"
def chuyen_anh_sang_base(img):
    try:
        with open(img, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
    except:
        return None
    
    return encoded_string 

def chuyen_base64_sang_anh(anh_base64):
    try:
        anh_base64 = np.fromstring(base64.b64decode(anh_base64), dtype=np.uint8)
        anh_base64 = cv2.imdecode(anh_base64, cv2.IMREAD_ANYCOLOR)
    except:
        return None
    return anh_base64
'''
@app.route('/nhandienkhuonmat', methods=['POST'] )
@cross_origin(origin='*')
def nhandienkhuonmat_process():
    # Đọc ảnh từ client gửi lên
    facebase64 = request.form.get('facebase64')
    
    # Chuyển base 64 về OpenCV Format
    #face = chuyen_base64_sang_anh(facebase64)
    
    # Trả về
    return str(facebase64)
'''

@app.route('/getBase64', methods=['GET'] )
@cross_origin(origin='*')
def getBase64_process():
    # Đọc ảnh từ client gửi lên
    facebase64 = request.args.get('imagebase64')
    
    # Chuyển base 64 về OpenCV Format
    #face = chuyen_anh_sang_base(facebase64)
    #cv2.imshow('Anh:', face)
    # Trả về
    return str(facebase64)

@app.route('/postBase64', methods=['POST'] )
@cross_origin(origin='*')
def postBase64_process():
    
    image = chuyen_anh_sang_base(img)
    #cv2.imshow('Anh:', face)
    # Trả về
    return image

# Start Backend
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='6868')