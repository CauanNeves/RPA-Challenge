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
    
class ConsultasPNCPsSpider(scrapy.Spider):
#identidade
    name= 'botconsultor'
#request
    def start_requests(self):
        urls= ['https://pncp.gov.br/app/editais?q=&status=recebendo_proposta&pagina=1']
        for url in urls:
            yield scrapy.Request(url= url, callback= self.parse, meta= {'next_url': url})
#response
    def parse(self, response):
        
        driver= start_driver()
        driver.get(response.meta['next_url'])
        
        #Pesquisando
        keywords = ['Dipirona sódica', 'Atenolol', 'Clonazepam']
        
        for keyword in keywords:
            #Abrindo Edital
            n_edital = 0
            contador_itens = 1
            while True:
                if contador_itens >= 100:
                    driver.execute_script('window.scrollTo({ top: 0, behavior: "instant" })')
                    driver.find_element(By.XPATH, '//a[@title="Editais"]').click()
                    break
                else:
                    driver.execute_script('window.scrollTo({ top: 0, behavior: "instant" })')
                    
                    wait_for_element(driver, By.XPATH, '//input[@id= "keyword"]').send_keys(f'{keyword}')
                    driver.find_element(By.CSS_SELECTOR, "label[for='status-todos']").click()
                    driver.find_element(By.XPATH, '//button[@aria-label = "Buscar"]').click()
                    sleep(2)
                    n_edital += 1
                    btn_edital = driver.execute_script(f'''
                    return document.evaluate(
                        '(//a[@title = "Acessar item."])[{n_edital}]', 
                        document, 
                        null, 
                        XPathResult.FIRST_ORDERED_NODE_TYPE, 
                        null
                        ).singleNodeValue;
                    ''')         
                    driver.execute_script('arguments[0].scrollIntoView({behavior: "instant", block: "center"});', btn_edital)
                    sleep(0.2)
                    btn_edital.click()

                    #No edital
                    wait_for_element(driver, By.XPATH, '//div[@class= "ng-star-inserted"]')

                    count_detail = 1
                    while True:
                        try:
                            #Fazendo um scroll até o botão, sem precisar de zoom ou um scroll fixo
                            if contador_itens <= 100:
                                sleep(0.8)
                                btn_detail = driver.execute_script(f'''
                                    return document.evaluate(
                                        '(//button[@class="br-button circle ng-star-inserted"])[{count_detail}]', 
                                        document, 
                                        null, 
                                        XPathResult.FIRST_ORDERED_NODE_TYPE, 
                                        null
                                        ).singleNodeValue;
                                    ''')
                                driver.execute_script('arguments[0].scrollIntoView({behavior: "instant", block: "center"});', btn_detail)
                                sleep(0.5)
                                btn_detail.click()
                                
                                #Para varrer
                                wait_for_element(driver, By.XPATH, '//div[@class= "br-modal modal-item-contrato"]')
                                sleep(0.5)
                                #Varrendo os dados
                                response_webdriver = Selector(text= driver.page_source)
                                for element in response_webdriver.xpath('//div[@class= "br-modal-body"]'):
                                    yield{
                                        'n_item': element.xpath('(//div[@class= "br-modal-body"]/div)[1]/text()').get(),
                                        'descricao': element.xpath('(//div[@class= "br-modal-body"]/div)[2]//span/text()').get(),
                                        'criterio_de_julgamento': element.xpath('((//div[@class= "br-modal-body"]/div)[3]/div)[1]//span/text()').get(),
                                        'situacao': element.xpath('((//div[@class= "br-modal-body"]/div)[3]/div)[2]//span/text()').get(),
                                        'tipo': element.xpath('((//div[@class= "br-modal-body"]/div)[3]/div)[3]//span/text()').get(),
                                        'categoria_do_itme_de_leilao': element.xpath('((//div[@class= "br-modal-body"]/div)[3]/div)[4]//span/text()').get(),
                                        'incentivo_basico': element.xpath('((//div[@class= "br-modal-body"]/div)[4]/div)[1]//span/text()').get(),
                                        'beneficio': element.xpath('((//div[@class= "br-modal-body"]/div)[4]/div)[2]//span/text()').get(),
                                        'margem_de_preferencia_normal': element.xpath('((//div[@class= "br-modal-body"]/div)[4]/div)[3]//span/text()').get(),
                                        'margem_de_preferencia_adicional': element.xpath('((//div[@class= "br-modal-body"]/div)[4]/div)[4]//span/text()').get(),
                                        'quantidade': element.xpath('((//div[@class= "br-modal-body"]/div)[5]/div)[1]//span/text()').get(),
                                        'unidade_de_medida': element.xpath('((//div[@class= "br-modal-body"]/div)[5]/div)[2]//span/text()').get(),
                                        'valor_unitario_estimado': element.xpath('((//div[@class= "br-modal-body"]/div)[5]/div)[3]//span/text()').get(),
                                        'valor_total_estimado': element.xpath('((//div[@class= "br-modal-body"]/div)[5]/div)[4]//span/text()').get(),
                                    }
                                    
                                driver.find_element(By.XPATH, '//button[@class= "br-button primary small m-2"]').click()
                                count_detail += 1
                                contador_itens += 1
                            else:
                                break
                        except:
                            try:
                                count_detail = 1
                                btn_next_page_scroll = driver.execute_script(f'''
                                            return document.evaluate(
                                                '//button[@id= "btn-next-page"]', 
                                                document, 
                                                null, 
                                                XPathResult.FIRST_ORDERED_NODE_TYPE, 
                                                null
                                                ).singleNodeValue;
                                            ''')
                                driver.execute_script('arguments[0].scrollIntoView({behavior: "instant", block: "center"});', btn_next_page_scroll)
                                sleep(0.2)
                                btn_next_page = driver.find_element(By.XPATH, '//button[@id= "btn-next-page"]')
                                is_disabled = btn_next_page.get_attribute('disabled') is not None
                            except:
                                driver.execute_script('window.scrollTo({ top: 0, behavior: "instant" })')
                                driver.find_element(By.XPATH, '//a[@title="Editais"]').click()
                                break
                            if is_disabled:
                                driver.execute_script('window.scrollTo({ top: 0, behavior: "instant" })')
                                driver.find_element(By.XPATH, '//a[@title="Editais"]').click()
                                break      
                            else:
                                btn_next_page.click()
        driver.quit()