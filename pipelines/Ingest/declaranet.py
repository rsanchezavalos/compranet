import time
import os
#import subprocess
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import requests
import sys
import xvfbwrapper 
from random import randint
from time import sleep



def Declaranet(funcionarios_list):
    print(path)
    driver.get(initial_url) 

    popup = driver.find_element_by_class_name('ui-icon-closethick')
    popup.click()

    for funcionario in funcionarios:
        # you'll have a list of names from the other table
        time.sleep(1)
        name = driver.find_element_by_id('form:nombresConsulta')        
        time.sleep(1)
        name.clear()
        name.send_keys(funcionario)
        time.sleep(3)
        btn = driver.find_element_by_id('form:buscarCosnsulta')
        btn.click()
        time.sleep(3)
        # Find all cases for that name
        results = driver.find_element_by_id('form:tblResultadoConsulta_data').find_elements_by_xpath("//tbody/tr/td")
        n_results = int(len(results)/2)
        print(n_results)

        for result in range(n_results):
            print("iteration number" + str(result))
            driver.implicitly_wait(160)
            driver.find_element_by_id('form:tblResultadoConsulta:{0}:j_idt53'.format(result)).click()
            driver.implicitly_wait(60)
            
            cv_results = driver.find_element_by_id("form:tblResultado_data").find_elements_by_xpath("//tr[@data-ri]")
            cv_n_results = int(len(cv_results))

            for cv in range(cv_n_results):
                print("iteration number" + str(result) + " - cv number: " + str(cv))
                cve = funcionario +"-"+ cv_results[cv].text
                cve = cve.replace(" ", "-").replace("/", "-")
                driver.implicitly_wait(160)

                try:
                    driver.find_element_by_id('form:tblResultado:{0}:idButtonConsultaAcuse'.format(cv)).click()
                    driver.implicitly_wait(160)

                    cookies = {
                        'JSESSIONID': driver.get_cookies()[1]["value"],
                        '_ga': driver.get_cookies()[0]["value"],
                        '_gat': '1',
                    }
                    headers = {
                        'Accept-Encoding': 'gzip, deflate, sdch',
                        'Accept-Language': 'es-MX,es;q=0.8,es-419;q=0.6,en;q=0.4',
                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                        'Accept': '*/*',
                        'Referer': 'http://servidorespublicos.gob.mx/registro/consulta.jsf',
                        'Connection': 'keep-alive',
                    }
                    sleep(randint(0,100)/100)

                    temp = requests.get('http://servidorespublicos.gob.mx/consulta.pdf', headers=headers, cookies=cookies)
                    print(temp)

                    with open(path + cve + ".pdf", 'wb') as f:
                        f.write(temp.content)
                        print(path + cve + ".pdf")   


                    time.sleep(1)
                    temp  = driver.find_element_by_id("form:buscar")
                    temp.send_keys(Keys.ESCAPE)

                except:
                    pass        
            driver.find_element_by_id("form:buscar").click()
        driver.find_element_by_id("form:buscar").click()

if __name__ == "__main__":
    # Define Path
    path = "/home/baco/temp/cvs/"
    initial_url ="http://servidorespublicos.gob.mx"

    funcionarios = sys.argv[1].split(',')
    funcionarios_list = [x for x in funcionarios]
    print(funcionarios_list)

    # Start Display
    display = xvfbwrapper.Xvfb()
    display.start()
    chromedriver = "/usr/bin/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    chromeOptions = webdriver.ChromeOptions()
    mime_types = "application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf,application/vnd.adobe.xdp+xml"
    prefs = {"browser.download.folderList":2, "browser.download.dir": u'/home/ubuntu', "browser.download.manager.showWhenStarting":False,"browser.helperApps.neverAsk.saveToDisk":mime_types,"pdfjs.disabled":"true","plugins.plugins_list": [{"enabled":False,"name":"Chrome PDF Viewer"}],"plugin.disable_full_page_plugin_for_types":mime_types}
    chromeOptions.add_experimental_option("prefs",prefs)
    #self.driver = webdriver.Chrome(chromedriver,chrome_options=chromeOptions)
    driver = webdriver.Chrome(chromedriver,chrome_options=chromeOptions)
    driver = webdriver.Chrome()
    driver.implicitly_wait(60)

    # Run function 
    Declaranet(funcionarios_list)





#######################################################
#######################################################
