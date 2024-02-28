import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import os 
from dotenv import load_dotenv

load_dotenv()

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"A Função {func.__name__} levou {elapsed_time} segundos para executar.")
        return result

    return wrapper


PATH = os.getenv("PROGRAM_PATH")
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_experimental_option("debuggerAddress", "localhost:9191")
driver = webdriver.Chrome(PATH, options=chrome_options)


#driver.get("https://stake.com/pt/casino/games/roulette")
#time.sleep(3)

#################################################################################
#Recomendações, tirar a animação e ativar o modo rápido, dessa forma seria insta a aposta
#################################################################################

def aposta():
    
    aposta = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[4]/div/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div/div/div/div/div[1]/div[1]/button')
    aposta.click()
    time.sleep(0.1)

def scrap_result():
    resultado = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[4]/div/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div/div/div/div/div[1]/div[2]/div/div/div[1]/div/span')
    background_color = resultado.value_of_css_property("background-color")
    return  background_color

def dobra(num):
    for i in range(num):
        dobra = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[4]/div/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div/div/div/div/div[1]/div[1]/label/div/div[2]/button[2]/span')
        dobra.click()
        time.sleep(0.1)

def divide(num):
    for i in range(num):
        #/html/body/div[1]/div[2]/div[2]/div[4]/div/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div/div/div/div/div[1]/div[1]/label/div/div[2]/button[1]/span
        meio = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[4]/div/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div/div/div/div/div[1]/div[1]/label/div/div[2]/button[1]/span')
        meio.click()
        time.sleep(0.1)

def aumenta():
    dobra = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[4]/div/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div/div/div/div/div[1]/div[2]/div/div/div[3]/button[4]/div[2]')
    dobra.click()
    time.sleep(0.1)

def diminui():
        
    meio = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[4]/div/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div/div/div/div/div[1]/div[2]/div/div/div[4]/button[2]/span')
    meio.click()
    time.sleep(0.1)
    aumenta()


cores = {"preto":"rgba(47, 69, 83, 1)","vermelho":"rgba(254, 34, 71, 1)"}

cor = "vermelho"
rgb = cores[cor]

df = pd.DataFrame([], columns = ['valor aposta',"resultado","balanco","num_aposta"])

contador,erros = 0,0
balanco = float(driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[3]/div/div/div/div[2]/div/div/div/button/span/div/div/span[1]/span/span').text.replace("R$",""))

#Martingale aplicado
row = []
while True:
    valor_aposta = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[4]/div/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div/div/div/div/div[1]/div[1]/label/span/div[2]/div/div').text.replace("R$","")
    aposta()
    time.sleep(0.5)
    roleta = scrap_result()
    if rgb == roleta:
        if erros != 0:
            divide(erros)
        erros = 0 
    else:
        dobra(1)
        erros += 1
    if erros == 8:
        print("muitas perdas")
        break


    conta = float(driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[3]/div/div/div/div[2]/div/div/div/button/span/div/div/span[1]/span/span').text.replace("R$",""))
    row.append(valor_aposta)
    row.append(roleta)
    row.append(conta-balanco)
    row.append(contador)
    contador += 1
    df.loc[len(df)] = row
    row = []
    if contador == 100:
        break

df.to_excel("historico_stake_roleta-3.xlsx")


'''
#
while True:
    
    aposta()
    
    time.sleep(0.5)
    roleta = scrap_result()
    if rgb == roleta:
        if erros != 0:
            aumenta()
        erros = 0 
    else: 
        diminui()
        erros += 1

    if erros == 4:
        print("muitas perdas")
        break
    contador += 1
'''
