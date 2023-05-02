#!/usr/bin/env python3
import cv2
import os
from PIL import Image
import pytesseract

os.chdir('<insert_path>')

days = ['monday', 'friday', 'thursday', 'wednesday', 'tuesday', 'monday', 'friday', 'thursday', 'wednesday', 'tuesday', 'monday']

for i in range(7):

    vidcap = cv2.VideoCapture('tet' + str(i) + '.mp4')
    success, image = vidcap.read()
    count = 0
    numOfFramesSave = 250
    print('I am in success with ' + str(i))
    print(success)
    if success == False:
        print('Cant find file, ' + str(i) + ' trying next file')
        continue
    while success:
        success, image = vidcap.read()
        if not success:
            break

        if (count % numOfFramesSave == 0):
            cv2.imwrite("%sframe%d.jpg" % (i, count), image)     # save frame as JPEG file

        if cv2.waitKey(10) == 27:
            break
        count += 1

    collect = []

    headlines = open('heads.txt', 'a')
    headlines.write(days[i])

    for j in range(500,7000,250):
        try:
            bali = Image.open('%sframe%d.jpg' % (i, j))
            cropIt = bali.crop((147,600,900,652))
            gray = cropIt.convert('L')
            bw = gray.point(lambda x: 0 if x < 128 else 255, '1')
            bw.save('2nrk' + str(j) + '.png')
            text = pytesseract.image_to_string(Image.open('2nrk' + str(j) +'.png'), lang="nor")
            headlines.write(text + '\n')
        except:
            print('%sframe%d.jpg not found' % (i, j))

    headlines.close()

