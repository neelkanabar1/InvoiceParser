# from msilib.schema import Directory
import os.path
import json
from os import path, remove
from posixpath import split

# from attr import fields
import cv2
import pytesseract
from pytesseract import Output
from pytesseract import image_to_string


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
