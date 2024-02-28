import cv2
import pyautogui
import numpy as np
import os
from dotenv import load_dotenv


load_dotenv()
PATH = os.getenv("PATH_DIR")
# Global variables
drawing = False  # True if mouse is pressed
ix, iy = -1, -1  # Initial coordinates of the mouse pointer
cropped_image = None  # Store the cropped image

# Mouse callback function
def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, img, cropped_image,i,PATH

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        #cv2.rectangle(img, (ix, iy), (x, y), (0, 0, 0), 2)
        cv2.imshow('image', img)

        # Crop and save the region of interest
        cropped_image = img[iy:y, ix:x]
        print(iy,y,ix,x)
        print(ix,iy,x-ix,y - iy)
        #C:\pyhton_esportivo\RoletaMartingale\crop_image.py
        cv2.imwrite(os.path.join(PATH,f"vermelho_{i}.png"), cropped_image)
        print("Cropped image saved successfully.")

# Read an image
        
for i in range(1,4):
    screenshot = pyautogui.screenshot()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_rectangle)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
