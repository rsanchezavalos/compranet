import scrapy 
from selenium import webdriver
import time

class Declaranet(scrapy.Spider):
    name = 'DeclaranetSpider'
    allowed_domains = ["http://servidorespublicos.gob.mx"]
    start_urls = ["http://servidorespublicos.gob.mx/"]

    def parse(self, response):
        self.driver.get(response.url)  # load response to the browser
        popup = self.driver.find_element_by_class_name('ui-icon-closethick')
        popup.click()
        time.sleep(5)
        
        name = self.driver.find_element_by_id('form:nombresConsulta')

        # Esto se tiene que hacer para todos los funcionarios de la lista
        name.send_keys("Paloma Merodio")
        btn = driver.find_element_by_id('form:buscarCosnsulta')
        btn.click()

        # Obtienes todos los resultados del nombre
        # contarlos
        response.id("form:tblResultadoConsulta_data")
        self.driver.close()

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(60)