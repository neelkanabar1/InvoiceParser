
from flask import Flask, render_template, request, redirect, flash, send_file
import shutil
from IPython.display import Image, clear_output
from os import path
from pytesseract import image_to_string
from pytesseract import Output
import pytesseract
from asyncio import subprocess
from flask import request
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
import os
import cv2
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secretkey'
# app.config['UPLOAD_FOLDER'] = 'static/uploaded_files'
# EXTENSIONS = ['pdf', 'png', 'jpeg', 'jpg', 'tiff']


# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSIONS


# @app.route('/', methods=["GET", "POST"])
# def index():
#     if request.method == 'POST':
#         file = request.files['file']
#         if file.filename == '':
#             flash('No file selected', 'error')
#             return render_template('index.html')
#         if not allowed_file(file.filename):
#             flash('Please upload the file in image or pdf format', 'error')
#             return render_template('index.html')
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             print(file)
#             subprocess.run("ls")
#             subprocess.run("python3", "/Users/neel.kanabar/Desktop/InvoiceParser/InvoiceParser/yolov5/detect.py", "--weights", "/Users/neel.kanabar/Desktop/InvoiceParser/best.pt",
#                            "--img", "416", "--source",
#                            os.path.join(app.config['UPLOAD_FOLDER'], filename), "--save-crop")


# @app.route('/return-files', methods=['GET'])
# def return_file():
#     obj = request.arg.get('obj')
#     loc = os.path.join("runs/detect", obj)
#     print(loc)
#     try:
#         return send_file(os.path.join("runs/detect", obj), attachment_filename=obj)
#     except Exception as e:
#         return str(e)


# if __name__ == '__main__':
#     app.run(debug=True)


app = Flask(__name__)
app.secret_key = "secret key"
UPLOAD_FOLDER = '/Users/neel.kanabar/Desktop/InvoiceParser/InvoiceParser/Upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DOWNLOAD_FOLDER = '/Users/neel.kanabar/Desktop/form16-main/form-16/json'
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'tiff'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/detect', methods=['POST'])  # 127.0.0.1:5000/
def detect():
    if request.method == 'POST':

        file = request.files['file']
        if file.filename == "":
            flash('No File has been Selected.', 'Error')
            return render_template('index.html')
        if not allowed_file(file.filename):
            flash('Please upload the file in image or pdf format', 'error')
            return render_template('index.html')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if path.exists("/Users/neel.kanabar/Desktop/InvoiceParser/InvoiceParser/yolov5/runs"):
                # path
                path = "/Users/neel.kanabar/Desktop/InvoiceParser/InvoiceParser/yolov5/runs"
                directory = "runs"
                # Parent Directory
                parent = "/Users/neel.kanabar/Desktop/InvoiceParser/InvoiceParser/yolov5"
                # Path
                path = os.path.join(parent, directory)
                # Remove the Directory if precvious runs are there
                shutil.rmtree(path)
            subprocess.run(['python3', '/Users/neel.kanabar/Desktop/InvoiceParser/InvoiceParser/yolov5/detect.py', '--weights', '/Users/neel.kanabar/Desktop/InvoiceParser/best.pt',
                            '--img', '416', '--source',
                            os.path.join(app.config['UPLOAD_FOLDER'], filename), '--save-crop'])
            if path.exists("/Users/neel.kanabar/Desktop/InvoiceParser/InvoiceParser/yolov5/runs"):
                Entities = {'Invoice-To': None, 'Invoice Number': None, 'Shipper Name': None, 'Consignee Name': None, 'Invoice Date': None,
                            'Ceva Ref': None, 'Description of Parts': None, 'Departure Date': None, 'Arrival Date': None, 'PO Number': None,
                            'Payment Due': None, 'Total Invoice': None}
                Dir = "/Users/neel.kanabar/Desktop/InvoiceParser/InvoiceParser/"
                Yolo_run = "yolov5/runs/detect/exp/crops"

                for i in Entities.keys():
                    # print(Dir + Yolo_run + '/' + i + '.jpg')
                    if path.exists(Dir + Yolo_run + '/' + i + '.jpg'):
                        img = cv2.imread(Dir + Yolo_run + '/' + i + '.jpg')
                        txt = image_to_string(img)
                        txt = os.linesep.join(
                            [text for text in txt.splitlines() if text.strip()]
                        )

                        words = txt.split('\n')
                        if i == "Invoice-To":
                            if "INVOICE TO" in words:
                                words.remove("INVOICE TO")
                        elif i == "Invoice Number":
                            if "INVOICE NUMBER" in words:
                                words.remove("INVOICE NUMBER")
                        elif i == "Shipper Name":
                            if "SHIPPER NAME" in words:
                                words.remove("SHIPPER NAME")
                        elif i == "Consignee Name":
                            if "CONSIGNEE NAME" in words:
                                words.remove("CONSIGNEE NAME")
                        elif i == "Invoice Date":
                            if "INVOICE DATE" in words:
                                words.remove("INVOICE DATE")
                        elif i == "Ceva Ref":
                            if "CEVA REF" in words:
                                words.remove("CEVA REF")
                        elif i == "Description of Parts":
                            if "DESCRIPTION OF GOODS" in words:
                                words.remove("DESCRIPTION OF GOODS")
                        elif i == "Departure Date":
                            if "DEPARTURE DATE" in words:
                                words.remove("DEPARTURE DATE")
                        elif i == "Arrival Date":
                            if "ARRIVAL DATE" in words:
                                words.remove("ARRIVAL DATE")
                        elif i == "PO Number":
                            if "PO Number" in words:
                                words.remove("PO Number")
                        elif i == "Payment Due":
                            words = txt.split(':')
                            if "PAYMENT DUE" in words:
                                words.remove("PAYMENT DUE")
                        elif i == "Total Invoice":
                            if "TOTAL INVOICE" in words:
                                words.remove("TOTAL INVOICE")
                            words.append("USD")
                        string = '\n'.join(words)
                        Entities[i] = string
                # for i in Entities.keys():
                #     print(i)
                #     if path.exists(Dir + Yolo_run + '/' + '{}.jpg'.format(i)):
                #         img = cv2.imread()
                #         i = image_to_string(img)
                #         i = os.linesep.join(
                #             [text for text in i.splitlines() if text.strip()]
                #         )
                #         print(i)
                # if path.exists(Directory + "yolov5/runs/detect/exp2/crops/Arrival Date.jpg"):
                #     img = cv2.imread(
                #         "/Users/neel.kanabar/Desktop/InvoiceParser/InvoiceParser/yolov5/runs/detect/exp2/crops/Arrival Date/28.jpg")
                #     Aggregate = image_to_string(img)

                #     Aggregate = os.linesep.join(
                #         [text for text in Aggregate.splitlines() if text.strip()])
                #     print(Aggregate)
                # if path.exists("/Users/neel.kanabar/Desktop/InvoiceParser/InvoiceParser/yolov5/runs/detect/exp/crops/Arrival Date.jpg"):
                #     img = cv2.imread(
                #         '/Users/neel.kanabar/Desktop/InvoiceParser/InvoiceParser/yolov5/runs/detect/exp/crops/Arrival Date.jpg')
                #     fields = image_to_string(img)
                #     fields = os.linesep.join(
                #         [text for text in fields.splitlines() if text.strip()]
                #     )
                #     print(fields)
                # print(Entities)

                with open("/Users/neel.kanabar/Desktop/InvoiceParser/json_response.json", "w") as outfile:
                    json.dump(Entities, outfile)

                # return render_template('index.html')

                #         if(filename[-3:] == 'PDF' or filename[-3:] == 'pdf'):
                #             images = convert_from_path(os.path.join(
                #                 app.config['UPLOAD_FOLDER'], filename))

                # @app.route('/info/<name>')  # 127.0.0.1:5000/info/
                # def function(name):
                #     return '<h1>Hello {}!</h1>'.format(name)


@app.route('/return-files', methods=['GET'])
def return_file():
    try:
        obj = request.arg.get('obj')

        obj = "/Users/neel.kanabar/Desktop/InvoiceParser/json_response.json"
        return send_file("/Users/neel.kanabar/Desktop/InvoiceParser/json_response.json")
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)
