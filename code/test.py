import time
import mod1
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
#import picamera
import cv2 as cv
import numpy as np
from collections import Counter
from imageai.Detection.Custom import CustomObjectDetection
import os

config = {
    "apiKey": "your api key",
    "authDomain": "YPUR AUTHDOMAIN",
    "databaseURL": "DB URL",
    "projectId": "PROJECT ID",
    "storageBucket": "STORAGE BUCKET",
    "messagingSenderId": "messagingSenderId"
}

def createExamples():
	numberArrayExamples = open('numArEx.txt','a')
	numbersWeHave = range(1,15)
	for eachNum in numbersWeHave:
		for furtherNum in numbersWeHave:
			imgFilePath = 'images'+str(eachNum)+'.'+str(furtherNum)+'.png'
			ei = Image.open(imgFilePath)
			eiar = np.array(ei)
			eiarl = str(eiar.tolist())
			lineToWrite = str(eachNum)+'::'+eiarl+'\n'
			numberArrayExamples.write(lineToWrite)
#createExamples()
statuss=0
#call above function first if you are using first time
def whatNumIsThis(filePath):
	global statuss
	matchedAr = []
	loadExamps = open('numArEx.txt','r').read()
	loadExamps = loadExamps.split('\n')
	i = Image.open(filePath)
	iar = np.array(i)
	iarl = iar.tolist()
	inQuestion = str(iarl)
	for eachExample in loadExamps:
		try:
			splitEx = eachExample.split('::')
			currentNum = splitEx[0]
			currentAr = splitEx[1]
			eachPixEx = currentAr.split('],')
			eachPixInQ = inQuestion.split('],')
			x = 0
			while x < len(eachPixEx):
				if eachPixEx[x] == eachPixInQ[x]:
					matchedAr.append(int(currentNum))
				x+=1
		except Exception as e:
			print(str(e))
	print(matchedAr)    
	x = Counter(matchedAr)
	print(x)
	status_1=x[1]
	statuss_2=x[2]
	if int(status_1)>int(statuss_2):
		statuss=1
		print(int(status_1))
	else:
		statuss=2
		print(int(statuss_2))
#and finally you can call number recognition function
#camera = picamera.PiCamera()
#size = 16, 16
damagedstat=""
def damagedetection():
	global damagedstat
	execution_path = os.getcwd()
	detector = CustomObjectDetection()
	detector.setModelTypeAsYOLOv3()
	detector.setModelPath(detection_model_path="detection_model-ex-028--loss-8.723.h5")
	detector.setJsonPath(configuration_json="detection_config.json")
	detector.loadModel()
	detections = detector.detectObjectsFromImage(input_image="d23.png", minimum_percentage_probability=60, output_image_path="image-new.png")
	for detection in detections:
		print(detection)
		print(detection["name"], " : ", detection["percentage_probability"], " : ", detection["box_points"])
		damagedstat=detection["name"]
while True:
	#print "LED off"
	#GPIO.output(18,GPIO.LOW)
	from firebase import firebase
	firebase = firebase.FirebaseApplication(' YOUR databaseURL HERE')
	take_pic_capture = firebase.get('/take_pic',None)
	print (take_pic_capture)
	if take_pic_capture=="1":
		#camera.capture('d.png')
		#im = Image.open("d.png")
		#im_resized = im.resize(size, Image.ANTIALIAS)
		#im_resized.save("d1.png", "PNG")
		damagedetection()
		whatNumIsThis('d23.png')
		#img=cv.imread('d.png')
		img=Image.open("d23.png")
		draw=ImageDraw.Draw(img)
		font=ImageFont.truetype("arial.ttf",20)
		#draw.text((10,25),"riped",font=font)
		#font=cv.FONT_HARSHEY_SIMPLEX
		if statuss==2:
			draw.text((30,25),"ripped",font=font)
			draw.text((30,40),str(damagedstat),font=font)
			#cv.putText(img,'riped',(230,50),font,0.8,(0,255,0),2,cv.LINE_AA)
			statuss=0
		if statuss==1:
			draw.text((30,25),"not ripped",font=font)
			draw.text((30,40),str(damagedstat),font=font)
			#cv.putText(img,'not riped',(230,50),font,0.8,(0,255,0),2,cv.LINE_AA)
			statuss=0
		img.save('d1.png')
		firebase_upload = mod1.lets_do_it(config)
		store_img = firebase_upload.storage()
		store_img.child("/d.png").put("d1.png")
