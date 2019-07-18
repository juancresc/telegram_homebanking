
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import time
import sys
class HB:
    def __init__(self):
        print("loading browser")
        opts = Options()
        opts.headless = True
        self.browser = Firefox(options=opts)
    
    def get_saldo(self, username, password):
        browser = self.browser
        print("loading website")
        browser.get('https://hb.redlink.com.ar/bna/login.htm')
        #enter username
        print("login in")
        input_username = browser.find_element_by_id('usuario')
        input_username.send_keys(username)
        button_ingresar_class = browser.find_elements_by_class_name('btn_ingresar')
        if len(button_ingresar_class) != 1:
            print("Should be 1 login button")
            exit
        button_ingresar = button_ingresar_class[0]
        button_ingresar.click()

        #wait
        time.sleep(3)

        input_pass = browser.find_element_by_id('clave')
        # if clave don't exists, wait and try again
        #attempts TODO
        attempts = 0
        while not input_pass:
            time.sleep(3)
            print('searching for clave')
            input_pass = browser.find_element_by_id('clave')
            attempts += 1
            if attempts > 4:
                print("No puedo ingresar clave")
                sys.exit()
        input_pass.send_keys(password)

        button_ingresar.click()

        #wait
        time.sleep(3)
        error_msg = "Su usuario ya se encuentra conectado al Home Banking"
        if error_msg in browser.page_source:
            print("ya está logueado")
            return "ya está logueado"
            sys.exit()

        tr_saldo_class = browser.find_elements_by_class_name('jqgrow')
        if not tr_saldo_class:
            print("no saldo table")
            return "no saldo table"
            btn_salir = browser.find_element_by_id('salir')
            btn_salir.click()
            sys.exit()

        tipo_caja = browser.find_element_by_css_selector('.jqgrow td:nth-of-type(1)').get_attribute('innerHTML')
        print(tipo_caja)

        moneda = browser.find_element_by_css_selector('.jqgrow td:nth-of-type(2)').get_attribute('innerHTML')
        print(moneda)

        cuenta = browser.find_element_by_css_selector('.jqgrow td:nth-of-type(4)').get_attribute('innerHTML')
        print(cuenta)

        saldo = browser.find_element_by_css_selector('.jqgrow td:nth-of-type(5)').get_attribute('innerHTML')
        print(saldo)
        res = (cuenta, moneda, tipo_caja, saldo, )
        #TODO ultimos movimientos
        #tr = browser.find_element_by_css_selector('.jqgrow')
        #tr.click()

        btn_salir = browser.find_element_by_id('salir')
        btn_salir.click()
        print("exit")
        return saldo

        