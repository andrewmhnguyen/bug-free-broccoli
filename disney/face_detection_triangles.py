import cv2
import dlib
import sys
import os
import math
from subprocess import Popen, PIPE
from PIL import Image


# Take in user input
img_name = input("Enter Image Name: ")
try:
    img = Image.open(img_name)
except IOError:
    print("==========================================")
    print("ERROR: Image cannot be open. Example input: test.jpg")
    print("Loading provided image...")
    img_name = 'test1.jpg'
    pass


# Image
user_img = cv2.imread(img_name)

# Find grayscale of image
gray = cv2.cvtColor(user_img, cv2.COLOR_BGR2GRAY)

# Extracting dlib's face detector and grab facial landmark
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("face_landmarks.dat")

faces = detector(gray)

# Capture the points on face
# 1-17 on Jaw (left to right)
# 18-22 on Left Eyebrow (left to right)
# 23-27 on Right Eyebrow (left to right)
# 28-31 on Nose Bridge (top to bottom)
# 32-36 on Nose (left to right)
# 37-42 on Left Eye (very left point to clockwise)
# 43-48 on Right Eye (very left point to clockwise)
# 49-60 on Outer Lip (very left point to clockwise)
# 61-68 on Inner Lip (very left point to clockwise)

jaw = []
brow_l = []
brow_r = []
bridge = []
nose = []
eye_l = []
eye_r = []
lip_out = []
lip_in = []
all_coord = []
for face in faces:
    landmark = predictor(gray, face)

    # Color and store face data
    count = 1
    for n in range(0,68):

        x = landmark.part(n).x
        y = landmark.part(n).y
        all_coord.append((x,y))

        if count <= 17: # Purple (Jaw)
            jaw.append((x,y))
            color = 255
            color1 = 0
            color2 = 100
        elif count <= 22: # Green (Left Eyebrow)
            brow_l.append((x,y))
            color = 100
            color1 = 255
            color2 = 170
        elif count <= 27: # Blue (Right Eyebrow)
            brow_r.append((x,y))
            color = 50
            color1 = 104
            color2 = 255
        elif count <= 31: # Light Blue (Nose Bridge)
            bridge.append((x,y))
            color = 235
            color1 = 169
            color2 = 169
        elif count <= 36: # Light Green (Nose)
            nose.append((x,y))
            color = 169
            color1 = 235
            color2 = 185
        elif count <= 42: # Light Blue (Left Eye)
            eye_l.append((x,y))
            color = 169
            color1 = 215
            color2 = 235
        elif count <= 48: # Pale Yellow (Right Eye)
            eye_r.append((x,y))
            color = 235
            color1 = 230
            color2 = 169
        elif count <= 60: # Light Blue (Outer Lip)
            lip_out.append((x,y))
            color = 255
            color1 = 204
            color2 = 153
        elif count <= 68: # Light Purple (Inner Lip)
            lip_in.append((x,y))
            color = 160
            color1 = 142
            color2 = 209
        count += 1

        cv2.circle(user_img, (x,y), 2, (color, color1, color2), -1)
    # Breaks after detecting the first face
    break



print("Jaw Coordinates:", jaw)
print("Left Brow Coordinates:", brow_l)
print("Right Brow Coordinates:", brow_r)
print("Bridge Coordinates:", bridge)
print("Nose Coordinates:", nose)
print("Left Eye Coordinates:", eye_l)
print("Right Eye Coordinates:", eye_r)
print("Outer Lip Coordinates:", lip_out)
print("Inner Lip Coordinates:", lip_in)

print("Number of Coordinates:",len(all_coord))
cv2.imshow("User_img", user_img)


def rect_contains(rect, point) :
    if point[0] < rect[0] :
        return False
    elif point[1] < rect[1] :
        return False
    elif point[0] > rect[2] :
        return False
    elif point[1] > rect[3] :
        return False
    return True

# Draw a point
def draw_point(img, p, color ) :
    cv2.circle( img, p, 2, color, -1)

# Draw delaunay triangles
def draw_delaunay(img, subdiv, delaunay_color ) :

    triangleList = subdiv.getTriangleList();
    size = img.shape
    r = (0, 0, size[1], size[0])

    for t in triangleList :
        
        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])
        
        if rect_contains(r, pt1) and rect_contains(r, pt2) and rect_contains(r, pt3) :
        
            cv2.line(img, pt1, pt2, delaunay_color, 1, cv2.LINE_AA, 0)
            cv2.line(img, pt2, pt3, delaunay_color, 1, cv2.LINE_AA, 0)
            cv2.line(img, pt3, pt1, delaunay_color, 1, cv2.LINE_AA, 0)

win_delaunay = "Delaunay Triangulation"

    # Turn on animation while drawing triangles
animate = True
    
    # Define colors for drawing.
delaunay_color = (255,255,255)
points_color = (0, 0, 255)

img_orig = user_img.copy();
    
    # Rectangle to be used with Subdiv2D
size = user_img.shape
rect = (0, 0, size[1], size[0])
    
    # Create an instance of Subdiv2D
subdiv = cv2.Subdiv2D(rect);

    
    # Read in the points
size=(user_img.shape[1],user_img.shape[0])
all_coord.append((1,1)) # top left corner ?
all_coord.append((size[0]-1,1)) # top right corner
all_coord.append(((size[0]-1)//2,1)) # 
all_coord.append((1,size[1]-1)) 
all_coord.append((1,(size[1]-1)//2))
all_coord.append(((size[0]-1)//2,size[1]-1))
all_coord.append((size[0]-1,size[1]-1)) # bottom right corner
all_coord.append(((size[0]-1),(size[1]-1)//2)) # middle

    # Insert points into subdiv
for p in all_coord :
    subdiv.insert(p)
        # Show animation
    if animate :
        img_copy = img_orig.copy()
            # Draw delaunay triangles
        draw_delaunay( img_copy, subdiv, (255, 255, 255) )
        cv2.imshow(win_delaunay, img_copy)
        cv2.waitKey(100)

    # Draw delaunay triangles
draw_delaunay( img_copy, subdiv, (255, 255, 255) )
cv2.imshow(win_delaunay, img_copy)

    # Draw points
for points in all_coord :
    draw_point(img_copy, points, (0,0,0))
    cv2.imshow(win_delaunay, img_copy)
    cv2.waitKey(100)



cv2.waitKey()