import scrapy 
from selenium import webdriver
import time

class Declaranet(scrapy.Spider):
    name = 'DeclaranetSpider'
    allowed_domains = ["http://servidorespublicos.gob.mx"]
    start_urls = ["http://servidorespublicos.gob.mx/"]

    def parse(self, response):
        #driver.get(response.url)
        self.driver.get(response.url)  # load response to the browser
        #popup = driver.find_element_by_class_name('ui-icon-closethick')
        popup = self.driver.find_element_by_class_name('ui-icon-closethick')
        popup.click()
        time.sleep(5)
        #name = driver.find_element_by_id('form:nombresConsulta')        
        name = self.driver.find_element_by_id('form:nombresConsulta')

        # Esto se tiene que hacer para todos los funcionarios de la lista
        name.send_keys("Paloma Merodio")
        btn = driver.find_element_by_id('form:buscarCosnsulta')
        btn.click()

        # Obtienes todos los resultados del nombre
        # contarlos
        import scrapy 
        from selenium import webdriver
        import time
        import tempfile
        import os

        name = 'DeclaranetSpider'
        allowed_domains = ["http://servidorespublicos.gob.mx"]
        start_urls = ["http://servidorespublicos.gob.mx/"]

        chromeOptions = webdriver.ChromeOptions()
        tgt = tempfile.mkdtemp()
        prefs = {"browser.download.folderList":2, "browser.download.manager.showWhenStarting":False,"browser.download.dir": "~/","browser.helperApps.neverAsk.saveToDisk":"application/pdf","pdfjs.disabled":"true","plugins.plugins_list": [{"enabled":False,"name":"Chrome PDF Viewer"}],"download.default_directory" : tgt}
        chromeOptions.add_experimental_option("prefs",prefs)
        driver = webdriver.Chrome(chrome_options=chromeOptions)

        driver.get(response.url)  # load response to the browser
        popup = driver.find_element_by_class_name('ui-icon-closethick')
        popup.click()
        name = driver.find_element_by_id('form:nombresConsulta')        
        name.send_keys("Paloma Merodio")
        btn = driver.find_element_by_id('form:buscarCosnsulta')
        btn.click()
        driver.implicitly_wait(60)
        driver.find_element_by_id('form:tblResultadoConsulta').click()
        driver.implicitly_wait(60)
        driver.find_element_by_id('form:tblResultadoConsulta:0:j_idt53').click()
        driver.implicitly_wait(60)
        driver.find_element_by_id('form:tblResultado:0:idButtonConsultaAcuse').click()
        driver.implicitly_wait(60)
        driver.get("http://servidorespublicos.gob.mx/consulta.pdf")
        ftgt = os.path.join(tgt,'consulta.pdf')
        
        self.driver.close()

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(60)