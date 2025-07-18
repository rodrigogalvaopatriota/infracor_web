import pandas as pd
from datetime import datetime
import streamlit as st
import altair as alt
import os


class Produtividade:

    def __init__(self):
        now = datetime.now()
        self.today = now.day
        self.atual_month = now.month
        self.atual_year = now.year

    
    # Configuração de página deve vir primeiro
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


    
    def read_files(self,file):
        #path = 'C:\\Users\\55419\\Documents\\icomon\\spot\\thiago\\Handover - TH\\Handover - TH\\robos\\resultados_produtividade\\resultado_produtividade.xlsx'
            # Carregar os dados do arquivo Excel
        
        
        df = pd.read_excel(f'{file}') 
        return df
    
    
    
    
    def produtividade(self,df_coordenador,df_top_bottom,df_resultado_coord_area,df_resultado_coord_campo,df_resultado_tecnico):

        tab1, tab2 = st.tabs([
            
            "Produtividade resultados",
            "Produtividade top/bottom/coordenador",
            
        ])


        with tab1:
           

            st.title("Produtividade resultados") 
            # Criar duas colunas para o layout
            col1_resultados, col2 = st.columns([4, 1])  # Ajuste as proporções como preferir (3:2, 1:1, etc.)
            #path = 'C:\\Users\\55419\\Documents\\icomon\\spot\\thiago\\Handover - TH\\Handover - TH\\robos\\resultados_produtividade\\resultado_produtividade.xlsx'
            # Carregar os dados do arquivo Excel
            #df_resultado = pd.read_excel(f'resultado_produtividade.xlsx') 
           
            #df_resultado = df_resultado.rename(columns={'Supervisor':'Coordenador'})
            #df_resultado['Início Execução'] = pd.to_datetime(df_resultado['Início Execução'],dayfirst=True)
            #df_resultado['ano'] = pd.to_datetime(df_resultado['Início Execução'],dayfirst=True).dt.year
            #df_resultado['dia'] = pd.to_datetime(df_resultado['Início Execução'],dayfirst=True).dt.day

            #df_resultado = df_resultado[df_resultado['ano']==self.atual_year]
            #df_resultado = df_resultado.rename(columns={
                #'Recurso de serviço: Matrícula WFM':'TR_tecnico',
                #'Recurso de serviço: Nome':'nome_tecnico'
            #})
            
            with st.sidebar:
                filter_coord_area = st.multiselect(
                    "Escolha os Coordenadores de área",
                    df_resultado_coord_area["Coordenador de área"].unique(),
                    default=df_resultado_coord_area["Coordenador de área"].unique()  # Seleciona todos os status por padrão
                    
                )

                filter_coord_campo = st.multiselect(
                    "Escolha os Coordenadores de campo",
                    df_resultado_coord_campo["Coordenador de campo"].unique(),
                    default=df_resultado_coord_campo["Coordenador de campo"].unique()  # Seleciona todos os status por padrão
                    
                )



            # Verificar se ambos os filtros possuem seleções
            if not filter_coord_area:
                st.error("Por favor, selecione pelo menos um status de distância.")
            
            
            else:
                # Filtrar os dados com base nas seleções
                data_filter_resultado_coord_area = df_resultado_coord_area[
                    #(df_resultado["Coordenador"].isin(filter_coordenador)) 
                    (df_resultado_coord_area["Coordenador de área"].isin(filter_coord_area))
                    #(df_resultado_coord_area["Coordenador de campo"].isin(filter_coord_campo))
                ]

                data_filter_resultado_coord_campo = df_resultado_coord_campo[
                    #(df_resultado["Coordenador"].isin(filter_coordenador)) 
                    (df_resultado_coord_campo["Coordenador de área"].isin(filter_coord_area))&
                    (df_resultado_coord_campo["Coordenador de campo"].isin(filter_coord_campo))
                ]

                data_filter_resultado_tecnico = df_resultado_tecnico[
                    #(df_resultado["Coordenador"].isin(filter_coordenador)) 
                    (df_resultado_tecnico["Coordenador de área"].isin(filter_coord_area))&
                    (df_resultado_tecnico["Coordenador de campo"].isin(filter_coord_campo))
                ]

              

                # Exibir gráficos e tabela
                with col1_resultados:
                    
                    st.markdown('<p style="font-size:30px; font-weight:bold;">Coordenador de área</p>', unsafe_allow_html=True)
                    st.dataframe(data_filter_resultado_coord_area, width=4000)  # Define a largura da tabela

                    st.markdown('<p style="font-size:30px; font-weight:bold;">Coordenador de campo</p>', unsafe_allow_html=True)
                    st.dataframe(data_filter_resultado_coord_campo, width=4000)

                    st.markdown('<p style="font-size:30px; font-weight:bold;">Técnico</p>', unsafe_allow_html=True)
                    st.dataframe(data_filter_resultado_tecnico, width=4000)

                    st.markdown('<p style="font-size:20px; font-weight:bold;">Visão diária em construção...</p>', unsafe_allow_html=True)






        
        with tab2:
           

            st.title("Produtividade top/bottom/coordenador") 
            # Criar duas colunas para o layout
            col1, col2 = st.columns([4, 1])  # Ajuste as proporções como preferir (3:2, 1:1, etc.)

            # Carregar os dados do arquivo Excel
            #df = pd.read_excel(f'resultado_coordenador_campo.xlsx')
            df =df_coordenador 
            df = df.rename(columns={'Supervisor':'Coordenador'})

            df_tecnico = df_top_bottom
            #df_tecnico = pd.read_excel(f'resultado_tecnico_campo.xlsx') 
            df_tecnico_top = df_tecnico.head(10)
            df_tecnico_bottom = df_tecnico.tail(10)
        
       

            # Verificar se ambos os filtros possuem seleções
            if not filter_coord_area:
                st.error("Por favor, selecione pelo menos um status de distância.")
            
            
            else:
                # Filtrar os dados com base nas seleções
                data = df[
                    (df["Coordenador"].isin(filter_coord_area)) 
                    #(df["nome_coordenador"].isin(coordenadores))
                ]

            


                # Exibir gráficos e tabela
                with col1:
                    
                    st.markdown('<p style="font-size:30px; font-weight:bold;">Coordenador</p>', unsafe_allow_html=True)
                    st.dataframe(df, width=4000)  # Define a largura da tabela
      
                    st.markdown('<p style="font-size:30px; font-weight:bold;">Técnico</p>', unsafe_allow_html=True)
                    st.markdown('<p style="font-size:20px; font-weight:bold;">Top</p>', unsafe_allow_html=True)
                    #st.write("### Top", width=4000)
                    st.dataframe(df_tecnico_top, width=4000)  # Define a largura da tabela
                    st.markdown('<p style="font-size:20px; font-weight:bold;">Bottom</p>', unsafe_allow_html=True)
                    #st.write("### Bottom", width=4000)
                    st.dataframe(df_tecnico_bottom, width=4000)  # Define a largura da tabela
                
         
class Dashboard:

    def __init__(self,path):
        self.path = path
        #self.df = TreatDataFrame()
        self.df = df = pd.read_excel(f'resultado_bas_corretivos_encerrados_regiao_prioridade.xlsx')
    
    
    
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

 
def main():
    path = 'C:\\Users\\55419\\Documents\\icomon\\spot\\thiago\\Handover - TH\\Handover - TH\\robos\\resultados_produtividade\\'
    path_nelson = 'C:\\Users\\55419\\Documents\\icomon\\spot\\thiago\\Handover - TH\\Handover - TH\\robos\\resultados_produtividade\\nelson\\'
    
    
    
    file_painel_geral_coord_campo = path+'painel_geral_Coordenador de campo.xlsx'
    file_painel_geral_coord_area = path+'painel_geral_Coordenador de área.xlsx'
    file_painel_geral_coord_tecnico = path+'painel_geral_nome_tecnico.xlsx'

    file_top_bottom = path_nelson+'resultado_tecnico_campo.xlsx'
    file_coordenador = path_nelson+'resultado_coordenador_campo.xlsx'
    
    executar = Produtividade()

    df_top_bottom = executar.read_files(file=file_top_bottom)
    df_coordenador = executar.read_files(file=file_coordenador)

    df_resultado_coord_campo = executar.read_files(file=file_painel_geral_coord_campo)
    df_resultado_coord_area = executar.read_files(file=file_painel_geral_coord_area)
    df_resultado_tecnico = executar.read_files(file=file_painel_geral_coord_tecnico)
    
    #executar.treat_df_result_to_principal_painel(df=df_resultado)
    executar.produtividade(
        df_coordenador=df_coordenador,
        df_top_bottom=df_top_bottom,
        df_resultado_coord_area=df_resultado_coord_area,
        df_resultado_coord_campo=df_resultado_coord_campo,
        df_resultado_tecnico=df_resultado_tecnico
        
    )

if __name__=='__main__':
    main()

    #streamlit run ponto_st.py