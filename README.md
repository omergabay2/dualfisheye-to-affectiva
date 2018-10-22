# dualfisheye-to-affectiva
this code was written in order to recognize multiple faces expressions with 360 dualfisheye cameras.
I used theta S camera - capturing 360 dualfisheye images with 15 fps.

I used ffmpeg to convert dualfisheye image to rectangular image.
the mapping file was created by "projection.c" program which creates the files
"fisheye_grid_ymap.pgm" and "fisheye_grid_xmap.pgm"
you can find the program at the link:
https://github.com/raboof/dualfisheye2equirectangular
you can create a mapping file for several cameras and resolutions.

in order to analayze expressions you need to get the affectiva ros node
https://www.affectiva.com/

face detection algorithem was taken from https://realpython.com/face-recognition-with-python/

## ***Running The Program***

***run:***
 
```
python run.py
```




###***face_publisher.py:***

capture dualfisheye photos, converting them to rectangular and, display the fixed picture,then recognize faces and publish them as image messages to ros topic "/usb_cam/image/raw".


###***Affectiva ros node (not mine):***

subscribing to image message in topic "/usb_cam/image/raw", then, recognize emotions and expression and publishing them to ***"/affdex_data"*** topic as affdex_msgs messages


###***aff_sub.py:***

subscribing to affectiva message ***"/affdex_data"*** and find Person index of each person in the room. then publish  the original affectiva data + Person Index as String to ***"/omer_data"*** topic.



###***plot_data.py:***

reading the ***data.txt*** file in live, getting the data and drawing real-time plots of expressions for each face.



###***The topic "/omer_data":***


time: from start running the code in seconds
Person ID: index number of the recognized person
location: x from 0 to 1920 of the person

Emotions:
between 0 and 100, except for valence (-100 and 100)
- 0: Joy
- 1: Anger
- 2: Disgust
- 3: Contempt
- 4: Engagement
- 5: Fear
- 6: Sadness
- 7: Surprise
- 8: Valence

Expressions: 
between 0 and 100
- 0: Attention
- 1: BrowFurrow
- 2: BrowRaise
- 3: ChinRaise
- 4: EyeClosure
- 5: InnerBrowRaise
- 6: LipCornerDepressor
- 7: LipPress
- 8: LipPucker
- 9: LipSuck
- 10: MouthOpen
- 11: NoseWrinkle
- 12: Smile
- 13: Smirk
- 14: UpperLipRaise
- 15: jawDrop
- 16: lipStretch
- 17: dimpler
- 18: cheekRaise
- 19: eyeWiden
- 20: lidTighten







