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

def get_countour_dim(gray_image):
    contours = cv2.findContours(gray_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    max_contours = max(contours, key=cv2.contourArea)
    return cv2.boundingRect(max_contours)

def get_mask_image(gray_image):
    mask = np.zeros(gray_image.shape, dtype="uint8")
    (x, y, w, h) = get_countour_dim(gray_image)
    cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)
    return mask

def get_image_2D_dim(image):
    return image.shape[:2]

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized
    

images = get_images("./images/real/*.jpg")
stitched_image = get_stitch_image(images)
gray_stitched_image = get_gray_image(stitched_image)
thresdold_image = get_threshold_image(gray_stitched_image)
mask_image = get_mask_image(thresdold_image)

# # Cropping
# print("[CONSOLE] Cropping Image")
# if stitched_image.shape[:2] == mask_image.shape[:2]:
#     (stitch_h, stitch_w) = get_image_2D_dim(stitched_image)
#     (mask_h, mask_w) = get_image_2D_dim(mask_image)
    
#     for h in range(mask_h, mask_h//2, -1):
#         resized_mask = image_resize(mask_image, height=h)
    
# else:
#     raise Exception("Starting mask and image does not equal")
    
show_image("hello", stitched_image)
# write_image("./output/thresh_img.jpg", thresdold_image)

