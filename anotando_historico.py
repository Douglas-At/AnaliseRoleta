import cv2
import pyautogui
import numpy as np
import pandas as pd
import os
import time
from dotenv import load_dotenv


load_dotenv()
PATH = os.getenv("PATH_DIR")

class OpenCv:
    def img_def(self,img_name):
        return os.path.join(os.getcwd(),img_name)
    
    def crop_img(self,img_name, cordenadas, output_name):
        image = cv2.imread(self.img_def(img_name))
        x1,y1,x2,y2 = cordenadas
        #cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cropped_image = image[y1:y2, x1:x2]
        cv2.imwrite(self.img_def(output_name), cropped_image)

    def screenshot(self):
        screenshot = pyautogui.screenshot()
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        return img
    
    def save_img(self,img,name):
        cv2.imwrite(self.img_def(name),img)


    def show_img(self,img):
        cv2.imshow("'-'", img)
        cv2.waitKey()
        cv2.destroyAllWindows()

    def save_number(self,cor,numero):
        global PATH
        region = (534,337,50,56)
        screenshot = pyautogui.screenshot(region=region)
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        cv2.imwrite(os.paht.join(PATH, fr'{numero}_{cor}.png'), screenshot)

    def screenshot_number(self):
        region = (534,337,50,56)
        screenshot = pyautogui.screenshot(region=region)
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        return screenshot
        

    

    def find_and_click(self,img2):
        """
        tela que acha e clicka no parametro de uma tela inteira
        """
        diver = cv2.imread(self.img_def(img2), cv2.IMREAD_UNCHANGED)
        w = diver.shape[1]
        h = diver.shape[0]

        while True:
            tela = self.screenshot()
            
            
            result = cv2.matchTemplate(tela, diver, cv2.TM_CCOEFF_NORMED)
            
            
            #check the values of max if >0,9 clicko 
            min_val,max_val, min_loc,max_loc = cv2.minMaxLoc(result)

            
            if max_val > 0.9:
                x, y = max_loc
            
                pyautogui.moveTo(x+(w>>1), y+(h>>1))
                pyautogui.click()
                break

    def hsv_indetifier(self,img_name):
        img = cv2.imread(self.img_def(img_name))
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = hsv_img[3, 3]
        return h,s,v

    def color_identifier(self,region, hsv_lower, hsv_upper,screenshot):
        """
        função para 
        """

        
        hsv_image = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
        hsv_lower_np = np.array(hsv_lower, dtype=np.uint8)
        hsv_upper_np = np.array(hsv_upper, dtype=np.uint8)

        mask = cv2.inRange(hsv_image, hsv_lower_np, hsv_upper_np)
        result = cv2.bitwise_and(screenshot, screenshot, mask=mask)

        return np.any(mask)



if __name__ == "__main__":
    ocv = OpenCv()

    preto = [127,60,38]
    preto_h = [i*1.05 for i in preto]
    preto_l = [i*0.95 for i in preto]
    #VERMELHO H 170 S 183 V 162
    vermelho = [170,183,162]
    vermelho_h = [i*1.05 for i in vermelho]
    vermelho_l = [i*0.95 for i in vermelho]
    #VERDE H 75 S 138 V 137
    verde = [75,138,137]
    verde_h = [i*1.05 for i in verde]
    verde_l = [i*0.95 for i in verde]
    
    #regiao = (335, 347, 532, 546)
    #confuso essa questão da area
    regiao = (537,335,51,15)
    #preto = cv2.imread(ocv.img_def("petro.png"))
    #vermelho = cv2.imread(ocv.img_def("vermelho.png"))
    #verde = cv2.imread(ocv.img_def("verde .png"))
    dict_teste = {"ocorrencia":[],"cor":[]}
    i = 0
    while True:
        ocv.find_and_click("cropped_1.png")
        time.sleep(0.8)
        while True:
            screenshot = pyautogui.screenshot(region=regiao)
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            foto_num = ocv.screenshot_number()
            start = time.time()
            if ocv.color_identifier(regiao, preto_l, preto_h,screenshot):
                print("preto")
                dict_teste['cor'].append("preto")
                cor = "preto"
                break
            elif ocv.color_identifier(regiao, vermelho_l, vermelho_h,screenshot):
                print("vermelho")
                dict_teste['cor'].append("vermelho")
                cor = "vermelho"
                break
            elif ocv.color_identifier(regiao, verde_l, verde_h,screenshot):
                print("verde")
                dict_teste['cor'].append("verde")
                cor = "verde"
                break
        cv2.imwrite(os.path.join(PATH,'registro_numeros',fr'{i}_{cor}.png'), foto_num)
        print(time.time()-start)
        dict_teste['ocorrencia'].append(i)
        i += 1
        d = pd.DataFrame(dict_teste)
        d.to_excel("registro_cores_20-02-2024.xlsx")

        if i%23 == 0:
            screenshot = pyautogui.screenshot()
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            cv2.imwrite(f"ultimos_numeros_{i/23}.png", screenshot)


