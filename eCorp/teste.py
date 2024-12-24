from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from time import sleep
import os
import scrapy
from scrapy.selector import Selector

def start_driver():
    chrome_options = Options()
    arguments = ['--lang=pt-BR', '--start-maximized']

    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': 'C:\\Users\\secretario',
        'download.directory_upgrade': True,
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,
    })

    driver = webdriver.Chrome(options=chrome_options)

    return driver

def wait_for_element(driver, by, value, timeout=60):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )
    

driver= start_driver()
driver.get('https://pncp.gov.br/app/editais?q=&status=recebendo_proposta&pagina=1')

#Pesquisando
wait_for_element(driver, By.XPATH, '//input[@id= "keyword"]').send_keys('Dipirona sódica')
driver.find_element(By.CSS_SELECTOR, "label[for='status-todos']").click()
driver.find_element(By.XPATH, '//button[@aria-label = "Buscar"]').click()

#Abrindo Edital
driver.execute_script("document.body.style.zoom='50%'")  
wait_for_element(driver, By.XPATH, '//a[@title = "Acessar item."]').click()

#No edital
wait_for_element(driver, By.XPATH, '//div[@class= "ng-star-inserted"]')
sleep(1)

contador = 1
while True:
    try:
        btn_detail = driver.execute_script(f'''
    return document.evaluate(
        '(//button[@class="br-button circle ng-star-inserted"])[{contador}]', 
        document, 
        null, 
        XPathResult.FIRST_ORDERED_NODE_TYPE, 
        null
    ).singleNodeValue;
''')
        driver.execute_script('arguments[0].scrollIntoView({behavior: "smooth", block: "center"});', btn_detail)
        btn_detail.click()
        
        #Para varrer
        wait_for_element(driver, By.XPATH, '//div[@class= "br-modal modal-item-contrato"]')
        sleep(0.2)
        #Varrendo os dados
        sleep(2)
        driver.find_element(By.XPATH, '//button[@class= "br-button primary small m-2"]').click()
        contador += 1
    except Exception as e:
        print(e)
        contador = 1
        btn_next_page = driver.find_element(By.XPATH, '//button[@id= "btn-next-page"]')
        is_disabled = btn_next_page.get_attribute('disabled') is not None
        
        if is_disabled:
            break
        else:
            btn_next_page.click()