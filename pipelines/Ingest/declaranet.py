#!/usr/bin/python2.7
"""Declaranet.py.

Este módulo crawlea de la página de declaranet.gob.mx los currículums históricos de 
los funcionarios pasados por el argumento. El código asume que el archivo se encuentra
en la carpeta ./data/servidores_crawl/

Ejemplo:
        $ python ./pipelines/Ingest/declaranet.py  Nombre-documento 


Atributos:
    Nombre-documento (str): Nombre del documento que tiene a los funcionarios por buscar.

    E.g.
        Isaac Cinta Sánchez,  Hector Merlin Marcial,  Lorenzo Gomez Vega,  Jaqueline Ramirez Galvan,  
        Arturo Daniel Almada Iberri,  Mario Zamora Gastelum,  Monica Romero Hernandez,  
        Luis Alberto Rodriguez Reyes,  Alfredo Torres Martinez,  Jose Luis  Velasquez  Salas ,  
        Miguel Angel  Gomez  Castillo ,  Mariana Lopez Suck,  Emilio Fueyo Saldaña

    Puedes descargar los nombres y acomodarlos para esta función de esta forma:
        "SELECT  nombre || primer_apellido || segundo_apellido  FROM raw.funcionarios \
        WHERE institucion LIKE '% SECRETARÍA DE COMUNICACIONES Y TRANSPORTES%';" | \
        uniq | awk 1 ORS=',' |  sed -e "s/[,| *,*]$//g;s/^//g;s/,$//g;" > \
        ./data/servidores_crawl/temp.txt

Output:
    Los currículums se descargan en la carpeta /tmp/$(time.strftime("%Y%m%d-%H%M%S"))
    Con el formato:
        nombre-institucion-tipo-fecha.pdf
    e.g.
        Arturo-Baca-SECRETARIA-DE-AGRICULTURA-GANADERIA-DESARROLLO-RURAL-PESCA-Y-ALIMENTACION-MODIFICACIÓN-20-05-2013.pdf

"""

import os
import time
import sys
import zipfile
import requests
import xvfbwrapper 
import subprocess
from random import randint
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def Declaranet(funcionarios_list,path):
    # Start Display driver
    
    display = xvfbwrapper.Xvfb()
    display.start()
    chromedriver = "/usr/bin/chromedriver"
    #chromedriver = "/usr/lib/chromium-browser/chromedriver"

    os.environ["webdriver.chrome.driver"] = chromedriver
    chromeOptions = webdriver.ChromeOptions()
    mime_types = "application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf,application/vnd.adobe.xdp+xml"
    prefs = {"browser.download.folderList":2, "browser.download.dir": u'/home/ubuntu', "browser.download.manager.showWhenStarting":False,"browser.helperApps.neverAsk.saveToDisk":mime_types,"pdfjs.disabled":"true","plugins.plugins_list": [{"enabled":False,"name":"Chrome PDF Viewer"}],"plugin.disable_full_page_plugin_for_types":mime_types}
    chromeOptions.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(chromedriver,chrome_options=chromeOptions)
    #driver = webdriver.Chrome()
    driver.implicitly_wait(100)


    print(path)
    driver.get(initial_url) 

    link = None

    while not link:
        try:
            link = driver.find_element_by_class_name('ui-icon-closethick')
            link.click()
        except NoSuchElementException:
            time.sleep(2)

    print('located')
    n = 0

    for funcionario in funcionarios_list:
        n += 1
        print(n)

        if n==5:
            funcionarios_list = funcionarios_list[5:]
            display.stop()
            Declaranet(funcionarios_list,path)
        else:
            print(n)
            pass

        try:
            print('intentando funcionario: ' + str(funcionario))
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

            if results[0].text == 'Sin Datos':
                fp = open ("funcionarios_sin_declaracion.txt","a")
                fp.write(funcionario+"\n")
                fp.closte()
                pass

            else:
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
            
            while not link:
                try:
                    driver.find_element_by_id("form:buscar").click()
                except NoSuchElementException:
                    print("looking for 'form:buscar'")
                    time.sleep(2)

        except:
            fp = open ("funcionarios_sin_declaracion.txt","a")
            fp.write(funcionario+"\n")
            fp.closte()
            pass

        
if __name__ == "__main__":
    # Get funcionarios as argument
    # funcionario file
    funcionario_path = sys.argv[1].split(',') if len(sys.argv) >= 2 else 'temp.txt'

    # Get funcionarios from file
    with open('./data/servidores_crawl/'+ str(funcionario_path), 'r') as myfile:
        funcionarios_list=myfile.read().replace('\n', '')
    funcionarios_list = funcionarios_list.split(',')

    initial_url ="http://servidorespublicos.gob.mx"
    timestr = time.strftime("%Y%m%d-%H%M%S")

    # create sin declaracion doc
    filename = "funcionarios_sin_declaracion.txt"
    if os.path.exists(filename):
        append_write = 'a'
    else:
        append_write = 'w' 
    highscore = open(filename,append_write)
    highscore.write("Crawl Date: " + str(timestr))
    highscore.close()

    # Path to be created
    path = "/tmp/" + timestr + "/"
    if not os.path.exists(path):
        os.makedirs(path)

    # Run crawler
    Declaranet(funcionarios_list,path)


#######################################################
#######################################################
#l = [funcionarios_list.index(i) for i in funcionarios_list if 'Berenice Olmos Sanchez' in i]
#l = [funcionarios_list.index(i) for i in funcionarios_list if 'Jose Manuel Solis Hernandez' in i]
#l = [funcionarios_list.index(i) for i in funcionarios_list if 'Juan Jose Gonzalez Peredo' in i]


