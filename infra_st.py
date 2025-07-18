import pandas as pd
from datetime import datetime
import streamlit as st
import altair as alt
import os

      
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