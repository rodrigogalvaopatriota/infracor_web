import pandas as pd
from datetime import datetime
import streamlit as st
import altair as alt
import os

      
class Dashboard:

    def __init__(self):
        
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

                filter_regiao = st.multiselect(
                    "Escolha as regioes",
                    self.df["regiao"].unique(),
                    default=self.df["regiao"].unique()  # Seleciona todos os status por padrão
                    
                )

                filter_nome_dia_abertura = st.multiselect(
                    "Escolha os dias de abertura",
                    self.df["nome_dia_abertura"].unique(),
                    default=self.df["nome_dia_abertura"].unique()  # Seleciona todos os status por padrão
                    
                )

                filter_nome_mes_abertura = st.multiselect(
                    "Escolha os dias de abertura",
                    self.df["nome_mes_abertura"].unique(),
                    default=self.df["nome_mes_abertura"].unique()  # Seleciona todos os status por padrão
                    
                )
                filter_hora_download = st.multiselect(
                    "Escolha a hora do download",
                    self.df["hora_download"].unique(),
                    default=self.df["hora_download"].unique()  # Seleciona todos os status por padrão
                    
                )

                filter_minuto_download = st.multiselect(
                    "Escolha o minuto do download",
                    self.df["minuto_download"].unique(),
                    default=self.df["minuto_download"].unique()  # Seleciona todos os status por padrão
                    
                )
        
        if not filter_prioridade:
                st.error("Por favor, selecione pelo menos um filtro.")

        else:
             # Filtrar os dados com base nas seleções
                df_filter_prioridade = self.df[
                    #(df_resultado["Coordenador"].isin(filter_coordenador)) 
                    (self.df["prioridade_ba"].isin(filter_prioridade))&
                    (self.df["uf"].isin(filter_uf))&
                    (self.df["regiao"].isin(filter_regiao))&
                    (self.df["nome_dia_abertura"].isin(filter_nome_dia_abertura))&
                    (self.df["nome_mes_abertura"].isin(filter_nome_mes_abertura))&
                    (self.df["hora_download"].isin(filter_hora_download))&
                    (self.df["minuto_download"].isin(filter_minuto_download))
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
    
    
    execute = Dashboard()
    execute.streamlit()
    
  
    
   

if __name__=='__main__':
    main()

    #streamlit run ponto_st.py