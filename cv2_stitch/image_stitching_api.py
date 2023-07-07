from fastapi import FastAPI, UploadFile, Response
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

app = FastAPI()

def convert_byte_to_arr(byte_image):
    print("Converting image from byte to np.arr")
    arr_image = np.array(Image.open(BytesIO(byte_image)))
    return arr_image

def convert_arr_to_byte(arr_image):
    print("Converting image from np.arr to byte")
    arr_image_cvt = cv2.cvtColor(arr_image, cv2.COLOR_RGB2BGR)
    success, byte_image = cv2.imencode('.jpg', arr_image_cvt)
    return byte_image.tobytes()

def stitch_image(images):
    print("Stitching images")
    stitcher = cv2.Stitcher.create()
    return stitcher.stitch(images)

@app.get("/")
async def home():
    print("hello")

@app.post("/stitch_image")
async def stitch_app(in_images:list[UploadFile]):
    #Add images to process
    images = []
    for in_image in in_images:
        byte_image = await in_image.read()
        arr_image = convert_byte_to_arr(byte_image)
        images.append(arr_image)
    # Stitch
    (status, stitched_image) = stitch_image(images)
    if status == 0:
        print("Stitch successful!")
        byte_stitched_image = convert_arr_to_byte(stitched_image)
        print('Done')
        return Response(byte_stitched_image, media_type="image/jpg")
    else:
        print("Stitch went wrong!")
        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)