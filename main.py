from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import time
from datetime import datetime as dt
import pandas as pd
import streamlit as st

import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# Função para aguardar o arquivo ser liberado
def aguardar_liberacao_arquivo(caminho_arquivo, tentativas=10, intervalo=1):
    for tentativa in range(tentativas):
        try:
            with open(caminho_arquivo, 'rb'):
                return True
        except PermissionError:
            print(f"Aguardando liberação do arquivo... tentativa {tentativa + 1}")
            time.sleep(intervalo)
    return False


# Classe de monitoramento
class MonitoramentoHandler(FileSystemEventHandler):

    def __init__(self, path_from, path_to,path_result):
        self.path_from = path_from
        self.path_to = path_to
        self.path_to_save_result = path_result
        self.execute_df = TreatDataFrame(path_result=self.path_to_save_result,path=self.path_to)
        
        
        #self.execute_df = TreatDataFrame(path=self.path_to,path_result=self.path_to_save_result)

    def on_created(self, event):
        if not event.is_directory:
            print(f"📄 Arquivo criado: {event.src_path}")

    def on_modified(self, event):
        self.today = dt.now()
        self.hora = self.today.hour
        self.minuto = self.today.minute

        if not event.is_directory:
            print(f"✍️ Arquivo modificado: {event.src_path}")

            if 'BAs Corretivos Encerrados' in event.src_path:
                print(f"🔍 Detectado arquivo alvo: {event.src_path}")

                # Aguardar liberação do arquivo
                if aguardar_liberacao_arquivo(event.src_path):
                    try:
                        destino = os.path.join(self.path_to, 'BAs Corretivos Encerrados.xlsx')
                        shutil.copy(src=event.src_path, dst=destino)
                        print(f"✅ Arquivo copiado com sucesso para: {destino}")
                        name_file = str(self.today).replace(':','_').replace('/','_').replace('.','_').replace('-','_')


                        df = pd.read_excel(f'{self.path_to}\\BAs Corretivos Encerrados.xlsx')
                        df['time'] = self.today
                       
                        
                        df.to_excel(f'{self.path_to}\\bas_corretivos_encerrados_{str(name_file)}.xlsx',index=None)
                        self.execute_df.treat_df()



                    except PermissionError as e:
                        print(f"❌ Permissão negada ao tentar copiar {event.src_path}: {e}")
                    except Exception as e:
                        print(f"❌ Erro inesperado: {e}")
                else:
                    print(f"❌ Arquivo {event.src_path} não pôde ser acessado após várias tentativas.")

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"🗑️ Arquivo deletado: {event.src_path}")

    def on_moved(self, event):
        if not event.is_directory:
            print(f"📦 Arquivo movido de {event.src_path} para {event.dest_path}")


class Navigate:

    def __init__(self,time_download,time_seconds_until_read_qr_code):
        self.time_download = time_download
        self.time_seconds_until_read_qr_code = time_seconds_until_read_qr_code
        #options = webdriver.FirefoxOptions()
        options = webdriver.ChromeOptions()
        #options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
        prefs = {
            "profile.default_content_settings.popups": 0,
            "download.prompt_for_download": False,
            "profile.content_settings.exceptions.automatic_downloads.*.setting": 1,
            "download.directory_upgrade": True,
        }

        options.add_experimental_option("prefs", prefs)
        #set_browser_view = input('Deseja abrir o navegador? (s/n): ')
        #if set_browser_view.lower() == 'n':
            #options.add_argument("--headless")

        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=700,700")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        #self.browser = webdriver.Firefox(options=options)
        self.browser = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.browser, 20)
        self.browser.get('https://infracor.interno.srv.br/')
        time.sleep(self.time_seconds_until_read_qr_code)
    
    def go_bases_corretivos(self):
        
            
            while True:

                try:
                    self.browser.get('https://infracor.interno.srv.br/bases/corretivo#')
                    # Selecionar regiões
                    print(f'will try select no ')
                    time.sleep(5)
                    #select_element_regiao.select_by_visible_text('NO')
                    #select_element_regiao.select_by_value('NO')
                    #time.sleep(5)
                    #print(f'will try select sul ')
                    #select_element_regiao.select_by_visible_text('SUL')
                    #select_element_regiao.select_by_value('SUL')
                    time.sleep(5)

                    

                    try:
                        script_reload = """
                        window.location.reload();

                        """
                    
                        self.browser.execute_script(script=script_reload)
                        time.sleep(5)
                    except Exception as e:
                        print(f'ERROR em reload')
                    
                    
                    try:
                        script = """
                        

                        const select = document.getElementById('regiao');
                        for (const option of select.options) {
                            if (option.text.toUpperCase().includes('NO') || option.text.toUpperCase().includes('SUL')) {
                                option.selected = true;
                            }
                        }
                        select.dispatchEvent(new Event('change', { bubbles: true }));
                        """
                        self.browser.execute_script(script)
                        time.sleep(5)
                    except Exception as e:
                        print(f'ERROR em selecionar sul e no.')
                    
                    #btn_enviar = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[2]/div[1]/div[2]/button')))

                    try:
                        script_click_buscar = """
                        
                        
                                btn_buscar = document.getElementById('buscar')
                                if(btn_buscar){
                                        btn_buscar.click()

                                    }

                        """
                        
                        
                        
                        self.browser.execute_script(script_click_buscar)
                        
                        print(f'btn buscar clicado')
                    except Exception as e:
                        print(f'ERRO em clicar em buscar: {e}')


                    #print(f'select_element_regiao: {select_element_regiao}')
                except Exception as e:
                    print(f'ERRO em select_element_regiao NO OU SUL')
                # Clicar no botão enviar
                #btn_enviar = self.wait.until(EC.element_to_be_clickable((By.ID, 'buscar')))
                #btn_enviar = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[2]/div[1]/div[2]/button')))
                #print(f'btn_enviar: {btn_enviar}')
                #btn_enviar.click()

                #self.browser.execute_script(script_click_buscar)
                #print(f'btn_enviar clicado')
                time.sleep(30)  # Aguarda carregamento dos dados

                # Aguarda até que o botão de exportar esteja visível
                try:
                    self.wait.until(
                        EC.visibility_of_element_located((By.XPATH, "/html/body/main/div[2]/div[2]/div/div/div[2]/div/div/div/div/div[6]/div/div/div[1]/div/table"))
                    )
                    print("Botão de exportar visível. Página carregada.")

                    
                    try:
                        #btns_export = self.browser.find_elements(By.TAG_NAME, 'i')
                        #if btns_export:
                           # btns_export[0].click()
                            #print(f"Botão clicado em {datetime.now().strftime('%H:%M:%S')}")
                        #else:
                            #print(f"Botão não encontrado em {datetime.now().strftime('%H:%M:%S')}")

                        script_btn_download = """
                        
                            const btn_download = document.getElementsByTagName('i');
                            if (btn_download[0]) {
                                
                                btn_download[0].click();
                                console.log('⬇️ Download realizado');
                            }
                            """
                        self.browser.execute_script(script_btn_download)
                        time.sleep(self.time_download)
                    
                    except TimeoutException:
                        print("Não carregou btns_export no tempo esperado.")
                
                
                except TimeoutException:
                    print("Não carregou a tabela wait.until  no tempo esperado.")

      

    def loop_click_export(self):
        try:
            while True:
                btns_export = self.browser.find_elements(By.TAG_NAME, 'i')
                if btns_export:
                    btns_export[0].click()
                    print(f"Botão clicado em {datetime.now().strftime('%H:%M:%S')}")
                else:
                    print(f"Botão não encontrado em {datetime.now().strftime('%H:%M:%S')}")

                time.sleep(60)  # Aguarda 60 segundos (1 minuto)

        except KeyboardInterrupt:
            print("Loop interrompido manualmente.")
        except Exception as e:
            print(f"Ocorreu um erro no loop: {e}")

    def close(self):
        self.browser.quit()


class TreatDataFrame:

    def __init__(self,path,path_result):
        self.today = dt.now()
        self.hora = self.today.hour
        self.minuto = self.today.minute

        self.path = path
        self.path_result = path_result
        self.treat_data = TreatDate()
        self.execute_git = UpdateGit(path=self.path_result)
        

        
        pass

    def treat_df(self):
        
        
        #df.to_excel(f'bas_corretivos_encerrados_{name_file}')

        list_files = []
        for file in os.listdir(self.path):
            #print(f'path in treat_df: {self.path}//{file}')
            if 'bas_corretivos_encerrados_' in file:
                df = pd.read_excel(f'{self.path}//{file}')
               
                list_files.append(df)
        dfs = pd.concat(list_files)
        dfs['Abertura'] = pd.to_datetime(dfs['Abertura'])
        dfs['Promessa'] = pd.to_datetime(dfs['Promessa'])
        dfs['dataBaixa'] = pd.to_datetime(dfs['dataBaixa'])
        dfs['time'] = pd.to_datetime(dfs['time'])

        dfs['dia'] = dfs['Abertura'].dt.day
        dfs['den'] = 1
        dfs['hora_download'] = dfs['time'].dt.hour
        dfs['minuto_download'] = dfs['time'].dt.minute
        dfs['segundos_download'] = dfs['time'].dt.second



        self.treat_data.get_month_name_in_portuguese_df(df=dfs,name_column_data='Abertura',name_column_result='nome_mes_abertura')
        self.treat_data.get_day_in_portuguese_df(df=dfs,name_column_data='Abertura',name_column_day_week='nome_dia_abertura')

        dfs.to_excel(f'{self.path_result}\\resultado_bas_corretivos_encerrados.xlsx',index=None)
        columns = dfs.columns
        
        dfs_regiao_prioridadeBa = dfs.groupby(['regiao','uf','Loc.','Est.','prioridade_ba','nome_dia_abertura','nome_mes_abertura','Cos','breve_descr_problema','time','hora_download','minuto_download'],as_index=False)[['den']].sum()
        
        dfs_regiao_prioridadeBa.to_excel(f'{self.path_result}\\resultado_bas_corretivos_encerrados_regiao_prioridade.xlsx',index=None)
        self.execute_git.update(file='resultado_bas_corretivos_encerrados_regiao_prioridade.xlsx')
        
        
        
        #dfs_uf = dfs.groupby(['uf'])[['']].count()

        
        return dfs_regiao_prioridadeBa
    
   

class TreatDate:
    def __init__(self):
        import locale
         
        self.value_locale = locale.setlocale(locale.LC_ALL,'pt_BR.UTF-8')

    def get_day_in_portuguese_df(self,df,name_column_data: str,name_column_day_week:str = 'nome_dia_semana'):
         
         """
         cria coluna com o nome do dia da semana em portugues.
         name_column_data = coluna data, no formado pd.to_datetime
         name_column_day_name = o nome que vc quer para o resultado, a coluna com o nome do dia da semana
         
         
         """
         
         
        
         df[name_column_day_week] = df[name_column_data].dt.day_name(locale=self.value_locale)
         return  df

   
    def get_month_name_in_portuguese_df(self, df, name_column_data: str, name_column_result: str = 'nome_mes'):
        """
        Adiciona uma coluna ao DataFrame com o nome do mês em português.

        Parâmetros:
        - df: DataFrame do pandas contendo os dados.
        - name_column_data: nome da coluna de datas (formato datetime).
        - name_column_result: nome da nova coluna a ser criada com o nome do mês (padrão: 'nome_mes').

        Retorna:
        - DataFrame com a nova coluna adicionada.
        """
        

        # Cria a nova coluna com o nome do mês em português
        df[name_column_result] = df[name_column_data].dt.month_name(locale = self.value_locale )

        return df


class Dashboard:

    def __init__(self,path):
        self.path = path
        self.df = TreatDataFrame()
    
    
    
    def streamlit(self):

      
        
        st.set_page_config(
            page_title="Infra cor Icomon",
            page_icon="📊",
            layout="wide",  # Alternativas: 'centered' ou 'wide'
        )

        st.image(
                    "ico.jpg",  # Caminho para a imagem
                    width=100,
                    #use_container_width=False,
                
                )

        with st.sidebar:
                filter_prioridade = st.multiselect(
                    "Escolha os ",
                    self.df["prioridade_ba"].unique(),
                    default=self.df["prioridade_ba"].unique()  # Seleciona todos os status por padrão
                    
                )

                filter_uf = st.multiselect(
                    "Escolha as ufs",
                    self.df["uf"].unique(),
                    default=self.df["uf"].unique()  # Seleciona todos os status por padrão
                    
                )
        
        if not filter_prioridade:
                st.error("Por favor, selecione pelo menos um filtro.")

        else:
             # Filtrar os dados com base nas seleções
                df_filter_prioridade = self.df[
                    #(df_resultado["Coordenador"].isin(filter_coordenador)) 
                    (self.df["prioridade_ba"].isin(filter_prioridade))
                    #(df_resultado_coord_area["Coordenador de campo"].isin(filter_coord_campo))
                ]

                df_filter_uf = self.df[
                    #(df_resultado["Coordenador"].isin(filter_coordenador)) 
                    (self.df["uf"].isin(filter_uf))
                    #(df_resultado_coord_area["Coordenador de campo"].isin(filter_coord_campo))
                ]


        st.markdown('<p style="font-size:30px; font-weight:bold;">Prioridade</p>', unsafe_allow_html=True)
        st.dataframe(df_filter_prioridade, width=4000) 

        st.markdown('<p style="font-size:30px; font-weight:bold;">Uf</p>', unsafe_allow_html=True)
        st.dataframe(df_filter_uf, width=4000) 

        

class UpdateGit:

    def __init__(self,path):
        self.path = path
        pass
    
    
    
    def update(self,file):
    
        import base64
        import requests

        # --- Configurações ---
        GITHUB_TOKEN = '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'
        REPO = 'rodrigogalvaopatriota/infracor_web'
        ARQUIVO = f'{file}'  # Ex: 'docs/relatorio.txt'
        NOVO_CONTEUDO = 'Conteúdo atualizado via Python.'

        # --- 1. Obter o SHA atual do arquivo ---
        url = f'https://api.github.com/repos/{REPO}/contents/{ARQUIVO}'
        headers = {'Authorization': f'token {GITHUB_TOKEN}'}

        res = requests.get(url, headers=headers)
        res.raise_for_status()
        sha_atual = res.json()['sha']

        # --- 2. Codificar novo conteúdo em base64 ---
        conteudo_base64 = base64.b64encode(NOVO_CONTEUDO.encode()).decode()

        # --- 3. Fazer o PUT para atualizar ---
        dados = {
            'message': 'Atualização via Python',
            'content': conteudo_base64,
            'sha': sha_atual
        }

        res = requests.put(url, headers=headers, json=dados)

        # --- 4. Verificar resposta ---
        if res.status_code == 200 or res.status_code == 201:
            print('✅ Arquivo atualizado com sucesso!')
        else:
            print(f'❌ Erro ao atualizar: {res.status_code}')
            print(res.text)




def main():
    

    
    
    path_from = os.path.join(
        'C:\\', 'Users', '55419', 'Downloads'
    )

    path_to = os.path.join(
        'C:\\', 'Users', '55419', 'Documents', 'icomon', 'spot', 'infracor_teste','files'
    )
    path_to_save_result = os.path.join(
        'C:\\', 'Users', '55419', 'Documents', 'icomon', 'spot', 'infracor_teste'
    )

    
    set_tipo = input('Deseja buscar dados no site? digite s para sim n para não: ')
    if set_tipo == 's':
        set_time_read_qr_code = input('Defina o tempo de espera do robô após  a leitura do qr code: ')
        set_time_read_qr_code = int(set_time_read_qr_code)
        
        set_time_download = input('Defina o tempo de download em segundos: ')
        set_time_download = int(set_time_download)

        execute_navigate = Navigate(time_download=set_time_download,time_seconds_until_read_qr_code=set_time_read_qr_code)

        # Cria o observador
        observer = Observer()
        handler = MonitoramentoHandler(path_from=path_from, path_to=path_to,path_result=path_to_save_result)

        # Agenda o monitoramento
        observer.schedule(handler, path=path_from, recursive=False)

        # Inicia o monitoramento
        observer.start()
        print("🚀 Monitoramento iniciado... Pressione CTRL+C para parar.")

        try:
            while True:
                time.sleep(1)
                execute_navigate.go_bases_corretivos()
            

        except KeyboardInterrupt:
            print("🛑 Encerrando monitoramento...")
            observer.stop()

        
        
        observer.join()

    set_teste = input('Deseja testar dfs? digite s para sim n para não: ')
    if set_teste == 's':
        #execute = TreatDataFrame(path=path_to,path_result=path_to_save_result)
        #execute.treat_df()
        execute_git = UpdateGit(path=path_to_save_result)
        execute_git.update(file='resultado_bas_corretivos_encerrados_regiao_prioridade.xlsx')

        #streamlit run ponto_st.py

    


    


if __name__ == '__main__':
    main()
