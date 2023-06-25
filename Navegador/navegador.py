from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import openpyxl
from selenium.webdriver.edge.options import Options

class iniciar():
    def __init__(self):
        #Configurações iniciais
        self.edge_path = 'msedgedriver.exe'
        self.service = Service(executable_path=self.edge_path)
        self.navegador = webdriver.Edge(service=self.service)
        
        #Definir tempo de espera
        self.wait = WebDriverWait(self.navegador, 30)

        #inciar pesquisa
        self.navegador.get("https://www.marinetraffic.com")
        self.navegador.set_window_size(1030, 700)

    def login(self):
        aceitar = self.wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')))
        self.navegador.execute_script('var minhaTag = document.querySelector("#qc-cmp2-ui > div.qc-cmp2-footer.qc-cmp2-footer-overlay.qc-cmp2-footer-scrolled > div > button.css-47sehv > span");minhaTag.click();')
        
        login = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/header/div/div/div[6]/div/div[2]/button')))
        login.click()

        email = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="email"]')))
        email.send_keys('hito@ufpa.br')

        senha = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]')))
        senha.send_keys('Naval123*')

        aceitar_login = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="login_form_submit"]')))
        aceitar_login.click()
        time.sleep(7)

    def extrair(self,imo,periodo):
        def salvar(dados):
            try:
                existing_df = pd.read_excel(rf'{imo}.xlsx')
            except FileNotFoundError:
                d = openpyxl.Workbook()
                d.save(f'{imo}.xlsx')
                existing_df = pd.read_excel(rf'{imo}.xlsx')

            novos_df = pd.DataFrame(dados)
            df_atualizado = pd.concat([existing_df, novos_df], ignore_index=True)
            df_atualizado.to_excel(rf'{imo}.xlsx', index=False)

        datas_geral = periodo.split('\n')

        for data in datas_geral:
            print(f'Dia: {data}')
            self.navegador.get(f"https://www.marinetraffic.com/en/data/?asset_type=vessel_positions&columns=timestamp,source,speed,course,lat_of_latest_position,lon_of_latest_position,show_on_live_map&quicksearch|begins|{imo}|quicksearch_vessel=313347&time_range|range_date|time_range={data},{data}")
            time.sleep(7)
            self.navegador.get(f"https://www.marinetraffic.com/en/data/?asset_type=vessel_positions&columns=timestamp,source,speed,course,lat_of_latest_position,lon_of_latest_position,show_on_live_map&quicksearch|begins|{imo}|quicksearch_vessel=313347&time_range|range_date|time_range={data},{data}")
            
            #Loop para pular de página (50itens)
            for y in range(10):  
                print(f'Página [{y+1}]')
                dados = {}

                #colocar para 50
                selec_tamanho = self.wait.until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="mui-1"]')))
                selec_tamanho.click()
                selec_50 = self.wait.until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="menu-"]/div[3]/ul/li[2]')))
                selec_50.click()

                #Raspar os dados da pagina
                try:
                    for linha in range(1,51):
                        #timestamp
                        timestamp = self.wait.until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="reporting_ag_grid"]/div/div[2]/div[2]/div/div[1]/div[2]/div[3]/div[1]/div/div[2]/div/div/div[{linha}]/div[1]/div')))
                        timestamp.text
                        dados.update({'timestamp':[timestamp.text]})

                        #speed
                        speed = self.wait.until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="reporting_ag_grid"]/div/div[2]/div[2]/div/div[1]/div[2]/div[3]/div[1]/div/div[2]/div/div/div[{linha}]/div[3]/div/div')))
                        speed.text
                        dados.update({'speed':[speed.text]})

                        #course
                        course = self.wait.until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="reporting_ag_grid"]/div/div[2]/div[2]/div/div[1]/div[2]/div[3]/div[1]/div/div[2]/div/div/div[{linha}]/div[4]/div/div')))
                        course.text
                        dados.update({'course':[course.text]})

                        #latitude
                        latitude = self.wait.until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="reporting_ag_grid"]/div/div[2]/div[2]/div/div[1]/div[2]/div[3]/div[1]/div/div[2]/div/div/div[{linha}]/div[5]/div/div')))
                        latitude.text
                        dados.update({'latitude':[latitude.text]})
                        
                        #longitude
                        longitude = self.wait.until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="reporting_ag_grid"]/div/div[2]/div[2]/div/div[1]/div[2]/div[3]/div[1]/div/div[2]/div/div/div[{linha}]/div[6]/div/div')))
                        longitude.text
                        dados.update({'longitude':[longitude.text]})
                        salvar(dados)

                except TimeoutException:
                    break
                #pular de pagina
                pular = self.wait.until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="reporting_ag_grid"]/div/div[2]/div[3]/div/div/div/div/div[3]/button[2]')))
                pular.click()

instancia = iniciar()
instancia.login()
entrada_periodo = """2023-02-10
        2023-02-11
        2023-02-12
        2023-02-13"""

instancia.extrair('313347', entrada_periodo)
