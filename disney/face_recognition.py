# Import Required Packages
# import numpy as np
import cv2
import dlib
import argparse
import time

# handle command line arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='path to image file')
ap.add_argument('-w', '--weights', default='./mmod_human_face_detector.dat',
                help='path to weights file')
args = ap.parse_args()

# load input image
image = cv2.imread(args.image)

if image is None:
    print("Could not read input image")
    exit()

# initialize hog + svm based face detector
hog_face_detector = dlib.get_frontal_face_detector()

# initialize cnn based face detector with the weights
cnn_face_detector = dlib.cnn_face_detection_model_v1(args.weights)

start = time.time()

# apply face detection (hog)
faces_hog = hog_face_detector(image, 1)

end = time.time()
print("Execution Time (in seconds) :")
print("HOG : ", format(end - start, '.2f'))

# loop over detected faces
for face in faces_hog:
    x = face.left()
    y = face.top()
    w = face.right() - x
    h = face.bottom() - y

    # draw box over face
    cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)

start = time.time()

# apply face detection (cnn)
faces_cnn = cnn_face_detector(image, 1)

end = time.time()
print("CNN : ", format(end - start, '.2f'))

# loop over detected faces
for face in faces_cnn:
    x = face.rect.left()
    y = face.rect.top()
    w = face.rect.right() - x
    h = face.rect.bottom() - y

     # draw box over face
    cv2.rectangle(image, (x,y), (x+w,y+h), (0,0,255), 2)

# write at the top left corner of the image
# for color identification
img_height, img_width = image.shape[:2]
cv2.putText(image, "HOG", (img_width-50,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0,255,0), 2)
cv2.putText(image, "CNN", (img_width-50,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0,0,255), 2)

# display output image
cv2.imshow("face detection with dlib", image)

# save output image
cv2.imwrite("cnn_face_detection.png", image)

# close all windows
cv2.destroyAllWindows()

# # Load Cascade
# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
#
# # Read input image and Convert into greyscale
# img = cv2.imread('test.jpg')
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
# # Debug: Prints True if faces are found
# test1 = face_cascade.load('haarcascade_frontalface_default.xml')
# print(test1)
#
# # Detect Face and form rectangles
# faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#
# # Dictionary to record face data
# face = {
#     "eyes_l": "none",
#     "eyes_r": "none",
#     "face": "none",
# }
#
# # Inside each face:
# for (x,y,w,h) in faces:
#     # Draw Rectangle
#     img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
#
#     roi_gray = gray[y:y+h, x:x+w]
#     roi_color = img[y:y+h, x:x+w]
#     eyes = eye_cascade.detectMultiScale(roi_gray)
#
#     # Inside each eyes
#     for (ex,ey,ew,eh) in eyes:
#
#         cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
#
# cv2.imshow('img',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
