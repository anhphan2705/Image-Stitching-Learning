import cv2
import numpy as np
import glob

# Get image paths and create a image list
print("[Accessing folder]")
image_paths = glob.glob("./images/cow/*.jpg")
images = []

print(image_paths)
# Add images into the memory
print("[Loading Images]")
for image_path in image_paths:
    image = cv2.imread(image_path)
    images.append(image)

# Stitching
print("[Stitching Images]")
stitcher = cv2.Stitcher_create()
(status, stitched_img) = stitcher.stitch(images)
    
# Display result
if status == 0:
    print("[Stitch successfully]")
    cv2.imshow("hello", stitched_img)
    cv2.imwrite("./output/stitched_cow.jpg", stitched_img)
    cv2.waitKey()
else:
    print("[Something went wrong]")

