import cv2
import dlib
import sys
import os
import math
import numpy as np
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

img_name2 = input("Enter Image Name: ")
try:
    img = Image.open(img_name2)
except IOError:
    print("==========================================")
    print("ERROR: Image cannot be open. Example input: test.jpg")
    print("Loading provided image...")
    img_name2 = 'test2.jpg'
    pass

# Image
user_img = cv2.imread(img_name)
user_img2 = cv2.imread(img_name2)

# Find grayscale of image
gray = cv2.cvtColor(user_img, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(user_img2, cv2.COLOR_BGR2GRAY)

# Extracting dlib's face detector and grab facial landmark
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("face_landmarks.dat")

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

jaw2 = []
brow_l2 = []
brow_r2 = []
bridge2 = []
nose2 = []
eye_l2 = []
eye_r2 = []
lip_out2 = []
lip_in2 = []
all_coord2 = []

def landmark_detection (img, grays, jaw, brow_l, brow_r, bridge, nose, eye_l, eye_r, lip_out, lip_in, all_coord) :
    faces = detector(grays)

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
    for face in faces:
        landmark = predictor(grays, face)

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

            #cv2.circle(img, (x,y), 2, (color, color1, color2), -1)
        # Breaks after detecting the first face
        break

    '''
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
    '''

    cv2.imshow("User_img", img)


landmark_detection (user_img, gray, jaw, brow_l, brow_r, bridge, nose, eye_l, eye_r, lip_out, lip_in, all_coord) 
landmark_detection (user_img2, gray2, jaw2, brow_l2, brow_r2, bridge2, nose2, eye_l2, eye_r2, lip_out2, lip_in2, all_coord2) 


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
def draw_delaunay(img, subdiv, delaunay_color, dictionary ) :
    triangleList = subdiv.getTriangleList();
    triangle_list = []
    size = img.shape
    r = (0, 0, size[1], size[0])

    for t in triangleList :
        
        pt1 = (int(t[0]), int(t[1]))
        pt2 = (int(t[2]), int(t[3]))
        pt3 = (int(t[4]), int(t[5]))
        
        if rect_contains(r, pt1) and rect_contains(r, pt2) and rect_contains(r, pt3) :
            cv2.line(img, pt1, pt2, delaunay_color, 1, cv2.LINE_AA, 0)
            cv2.line(img, pt2, pt3, delaunay_color, 1, cv2.LINE_AA, 0)
            cv2.line(img, pt3, pt1, delaunay_color, 1, cv2.LINE_AA, 0)
            triangle_list.append((dictionary[pt1],dictionary[pt2],dictionary[pt3]))
    
    dictionary = {}
    return triangle_list


def delaunay_window(img, all_coord, subdiv, dictionary) :
    win_delaunay = "Delaunay Triangulation"
    # Turn on animation while drawing triangles
    animate = True
    
    # Define colors for drawing.
    delaunay_color = (255,255,255)
    points_color = (0, 0, 255)

    img_orig = img.copy();
    
    # Rectangle to be used with Subdiv2D
    size = img.shape
    rect = (0, 0, size[1], size[0])
    
    # Create an instance of Subdiv2D
    subdiv = cv2.Subdiv2D(rect);
    
    # Read in the points
    size=(img.shape[1],img.shape[0])
    all_coord.append((1,1)) # top left corner ?
    all_coord.append((size[0]-1,1)) # top right corner
    all_coord.append(((size[0]-1)//2,1)) # 
    all_coord.append((1,size[1]-1)) 
    all_coord.append((1,(size[1]-1)//2))
    all_coord.append(((size[0]-1)//2,size[1]-1))
    all_coord.append((size[0]-1,size[1]-1)) # bottom right corner
    all_coord.append(((size[0]-1),(size[1]-1)//2)) # middle

    # Make a points list and a searchable dictionary. 
    points=[(int(x[0]),int(x[1])) for x in all_coord]
    dictionary={x[0]:x[1] for x in list(zip(points,range(76)))}


    
    # Insert points into subdiv
    for p in all_coord:
        subdiv.insert(p)
        # Show animation
        if animate :
            img_copy = img_orig.copy()
                # Draw delaunay triangles
            draw_delaunay( img_copy, subdiv, (255, 255, 255), dictionary )
            cv2.imshow(win_delaunay, img_copy)
            cv2.waitKey(100)

    # Draw delaunay triangles
    triangle_list = draw_delaunay( img_copy, subdiv, (255, 255, 255), dictionary )
    cv2.imshow(win_delaunay, img_copy)

    # Draw points
    for points in all_coord :
        draw_point(img_copy, points, (0,0,0))
    
    return triangle_list

subdiv = []
subdiv2 = []
dictionary = {}
dictionary2 = {}
    
#coordinates of the given image
triangle_list = delaunay_window(user_img, all_coord, subdiv, dictionary)
#coordinates of the matching one 
triangle_list2 = delaunay_window(user_img2, all_coord2, subdiv2, dictionary2)


def applyAffineTransform(src, srcTri, dstTri, size) :
    
    # Given a pair of triangles, find the affine transform.
    warpMat = cv2.getAffineTransform( np.float32(srcTri), np.float32(dstTri) )
    
    # Apply the Affine Transform just found to the src image
    dst = cv2.warpAffine( src, warpMat, (size[0], size[1]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101 )

    return dst


# Warps and alpha blends triangular regions from img1 and img2 to img
def morphTriangle(img1, img2, img, t1, t2, t, alpha) :

    # Find bounding rectangle for each triangle
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))
    r = cv2.boundingRect(np.float32([t]))


    # Offset points by left top corner of the respective rectangles
    t1Rect = []
    t2Rect = []
    tRect = []


    for i in range(0, 3):
        tRect.append(((t[i][0] - r[0]),(t[i][1] - r[1])))
        t1Rect.append(((t1[i][0] - r1[0]),(t1[i][1] - r1[1])))
        t2Rect.append(((t2[i][0] - r2[0]),(t2[i][1] - r2[1])))


    # Get mask by filling triangle
    mask = np.zeros((r[3], r[2], 3), dtype = np.float32)
    cv2.fillConvexPoly(mask, np.int32(tRect), (1.0, 1.0, 1.0), 16, 0);

    # Apply warpImage to small rectangular patches
    img1Rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
    img2Rect = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]]

    size = (r[2], r[3])
    warpImage1 = applyAffineTransform(img1Rect, t1Rect, tRect, size)
    warpImage2 = applyAffineTransform(img2Rect, t2Rect, tRect, size)

    # Alpha blend rectangular patches
    imgRect = (1.0 - alpha) * warpImage1 + alpha * warpImage2

    # Copy triangular region of the rectangular patch to the output image
    img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] = img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] * ( 1 - mask ) + imgRect * mask

alpha = 0.5
    
    # Convert Mat to float data type
img1 = np.float32(user_img)
img2 = np.float32(user_img2)

    # Read array of corresponding points
points1 = all_coord
points2 = all_coord2
points = []

    # Compute weighted average point coordinates
for i in range(0, len(points1)):
    x = ( 1 - alpha ) * points1[i][0] + alpha * points2[i][0]
    y = ( 1 - alpha ) * points1[i][1] + alpha * points2[i][1]
    points.append((x,y))


    # Allocate space for final output
imgMorph = np.zeros(img1.shape, dtype = img1.dtype)

# index of the triangles
# get a list of the triangles in an image
# for each triangle - go through it   
for i in range(len(triangle_list)):
    x = triangle_list[i][0]
    y = triangle_list[i][1]
    z = triangle_list[i][2]
    
    x = int(x)
    y = int(y)
    z = int(z)
            
    t1 = [points1[x], points1[y], points1[z]]
    t2 = [points2[x], points2[y], points2[z]]
    t = [ points[x], points[y], points[z] ]

            # Morph one triangle at a time.
    morphTriangle(img1, img2, imgMorph, t1, t2, t, alpha)

    # Display Result
cv2.imshow("Morphed Face", np.uint8(imgMorph))

cv2.waitKey()