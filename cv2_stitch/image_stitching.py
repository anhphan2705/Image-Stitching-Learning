import cv2
import glob

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

def get_stitch_image(image_list):
    print("[CONSOLE] Stitching Images")
    # Stitch
    stitcher = cv2.Stitcher.create()
    stitch_status, stitched_image = stitcher.stitch(image_list)
    # Output
    if stitch_status == 0:
        print("[CONSOLE] Stitch successfully")
        return stitched_image
    else:
        raise Exception("[Console] Stitch failed")
    
def get_threshold_image(gray_image):
    print("[CONSOLE] Thresholding image")
    return cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY)[1]

# Main
images = get_images("./images/real/*.jpg")
stitched_image = get_stitch_image(images)
# Output
show_image("Product", stitched_image)
write_image("./output/stitched_img.jpg", stitched_image)


