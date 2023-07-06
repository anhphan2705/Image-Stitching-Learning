import cv2
import glob
import numpy as np
import imutils


def show_image(header, image):
    print("[CONSOLE] Showing image")
    cv2.imshow(header, image)
    cv2.waitKey()
    
def write_image(directory, image):
    print("[CONSOLE] Saving image")
    cv2.imwrite(directory, image)

def get_images(directory):
    print("[CONSOLE] Accessing folder")
    image_paths = glob.glob(directory)
    print(image_paths)
    if len(image_paths) == 0:
        raise Exception("[CONSOLE] Invalid directory")
    images = []
    # Add image to memory
    print("[CONSOLE] Loading Images")
    for image_path in image_paths:
        image = cv2.imread(image_path)
        images.append(image)
    print(f"[CONSOLE] Loaded {len(images)} image(s)")
    return images

def get_gray_image(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

def get_stitch_image(image_list):
    print("[CONSOLE] Stitching Images")
    stitcher = cv2.Stitcher.create()
    stitch_status, stitched_image = stitcher.stitch(image_list)
    if stitch_status == 0:
        print("[CONSOLE] Stitch successfully")
        return stitched_image
    else:
        raise Exception("[Console] Stitch failed")
    
def get_threshold_image(gray_image):
    print("[CONSOLE] Thresholding image")
    return cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY)[1]

# def get_countour_dim(gray_image):
#     contours = cv2.findContours(gray_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     contours = imutils.grab_contours(contours)
#     max_contours = max(contours, key=cv2.contourArea)
#     return cv2.boundingRect(max_contours)

def get_image_2D_dim(image):
    return image.shape[:2]

def crop_image(image, factor):
    (h, w) = get_image_2D_dim(image)
    # Crop horizontally (width)
    amount_crop = w * (1-factor)
    w_upper = int(w - amount_crop//2)
    w_lower = int(amount_crop//2)
    # Crop vertically (height)
    amount_crop = h * (1-factor)
    h_upper = int(h - amount_crop//2)
    h_lower = int(amount_crop//2)
    return image[h_lower:h_upper, w_lower:w_upper]

def is_black_pixel_outline(threshold_image):
    # Find if there is black pixel on 4 sides
    (height, width) = get_image_2D_dim(threshold_image)
    # Lower side (0, w)
    for w in range(0, width):
        if all(threshold_image[0, w] == [0, 0]):
            print(0, w)
            return True
    # Upper side (h, w)
    for w in range(0, width):
        if all(threshold_image[height-1, w] == [0, 0]):
            print(height-1, w)
            return True
    # Left side (h, 0)
    for h in range(0, height):
        if all(threshold_image[h, 0] == [0, 0, 0]):
            print(h, 0)
            return True
    # Right side (h, w)
    for h in range(0, height):
        if all(threshold_image[h, width-1] == [0, 0, 0]):
            print(h, width-1)
    return False
    
images = get_images("./images/real/*.jpg")
stitched_image = get_stitch_image(images)
gray_stitched_image = get_gray_image(stitched_image)
threshold_image = get_threshold_image(gray_stitched_image)
threshold_image_b = cv2.GaussianBlur(threshold_image, (3, 3), 0)
threshold_image = get_threshold_image(threshold_image_b)

# Cropping
print("[CONSOLE] Cropping Image")
threshold_image = crop_image(threshold_image, 0.815)
if is_black_pixel_outline(threshold_image):
    print("still black")
else:
    print("ya good")

    
show_image("hello", threshold_image)
write_image("./output/test_img.jpg", threshold_image)

