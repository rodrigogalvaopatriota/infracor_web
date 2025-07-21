import pandas as pd
from datetime import datetime
import streamlit as st
import altair as alt
import os

      
class Dashboard:

    def __init__(self):
        
        #self.df = TreatDataFrame()
        self.df = df = pd.read_excel(f'resultado_bas_corretivos_encerrados_regiao_prioridade.xlsx')
        self.df['den'] = self.df['den'].astype(float)
    
    
    
    def grafico_barras_prioridade_diaDaSemanaAbertura(self,data_chart,nome_x,nome_y):
        #nome_x = 'prioridade_ba'
        # Criar gráfico de barras com Altair
        bars = (
            #alt.Chart(data_menos_500)
            
            alt.Chart(data_chart)
            .mark_bar()
            .encode(
                x=alt.X(
                    f"{nome_x}:N",
                    sort=alt.EncodingSortField("den", op="sum", order="descending"),
                    #sort=alt.EncodingSortField("quantidade", op="sum", order="descending"),
                    title=f"{nome_x}",
                ),
                y=alt.Y(
                    "den:Q", title="Quantidade",
                    sort=alt.EncodingSortField("den", op="sum", order="descending"),
                    #text=alt.Text("den:Q", aggregate="sum", format=".0f")
                    
                
                ),
                color=f"{nome_y}:N",
                tooltip=[
                    alt.Tooltip(f"{nome_y}:N", title=f"{nome_y}"),
                    alt.Tooltip("den:Q", title="Quantidade"),
                    #alt.Tooltip("percentual:Q", title="Percentual (%)", format=".2f"),  # Mostrar o percentual
                ],
            )
            .properties(
                width=3000,
                #title="Quantidade de Colaboradores por Coordenador e Status de Distância",
            )
        )
        
        # Adicionar os rótulos de percentual
        text = (
            
            alt.Chart(data_chart)
            .mark_text(dy=-10, size=10, color="black")  # Ajusta a posição e aparência do texto
            .encode(
                x=alt.X("prioridade_ba:N"),
                #y=alt.Y("den:Q"),
               

                y=alt.Y("den:Q", aggregate="sum"),
                #text=alt.Text("den:Q", aggregate="sum", format=".0f"),
                detail=f"{nome_y}:N"
                #text=alt.Text("percentual:Q", format=".1f"), #  Formatar percentual com uma casa decimal
            )
        )
        
        # Combinar as barras e os rótulos no gráfico
        chart = bars + text
        #chart = bars
        return chart

    def grafico_barras(self,data_chart):

         # Criar o gráfico de barras
        chart = alt.Chart(data_chart).mark_bar(color='steelblue').encode(
            x=alt.X("prioridade_ba:N", sort='-y', title="prioridade_ba"),
            y=alt.Y("den:Q", title="Contagem de prioridade"),
            tooltip=["prioridade_ba", "den"]
        ).properties(
            width=800,  # Largura do gráfico
            height=400,  # Altura do gráfico
            title="Soma dos dias da semana por prioridade"
        )
        return chart


    def grafico_barras_(self, data_chart):
        bars = (
            alt.Chart(data_chart)
            .mark_bar()
            .encode(
                x=alt.X("prioridade_ba:N", title="Prioridade"),
                xOffset="nome_dia_abertura:N",  # <--- Essa linha é o segredo para barras lado a lado
                y=alt.Y("den:Q", title="Quantidade de Prioridades"),
                color="nome_dia_abertura:N",
                tooltip=[
                    alt.Tooltip("nome_dia_abertura:N", title="Dia da Semana Abertura"),
                    alt.Tooltip("den:Q", title="Quantidade"),
                ],
            )
            .properties(width=3000)
        )

        return bars

    
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
                    "Escolha as prioridades",
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
                    "Escolha os meses de abertura",
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

                filter_descricao_problema = st.multiselect(
                    "Escolha a descricao do problema",
                    self.df["breve_descr_problema"].unique(),
                    default=self.df["breve_descr_problema"].unique()  # Seleciona todos os status por padrão
                    
                )

                filter_est = st.multiselect(
                    "Escolha a Estação",
                    self.df["Est."].unique(),
                    default=self.df["Est."].unique()  # Seleciona todos os status por padrão
                    
                )
        
        if not filter_prioridade:
                st.error("Por favor, selecione pelo menos um filtro.")

        else:
             # Filtrar os dados com base nas seleções
                df_filter_prioridade = self.df[
                    
                    (self.df["prioridade_ba"].isin(filter_prioridade))&
                    (self.df["uf"].isin(filter_uf))&
                    (self.df["regiao"].isin(filter_regiao))&
                    (self.df["nome_dia_abertura"].isin(filter_nome_dia_abertura))&
                    (self.df["nome_mes_abertura"].isin(filter_nome_mes_abertura))&
                    (self.df["hora_download"].isin(filter_hora_download))&
                    (self.df["minuto_download"].isin(filter_minuto_download))&
                    (self.df["breve_descr_problema"].isin(filter_descricao_problema))&
                    (self.df["Est."].isin(filter_est))
                    #(df_resultado_coord_area["Coordenador de campo"].isin(filter_coord_campo))
                ]
         #dia da semana
        #regiao
        st.markdown('<p style="font-size:30px; font-weight:bold;">Prioridade e Região</p>', unsafe_allow_html=True)
        chart_regiao = self.grafico_barras_prioridade_diaDaSemanaAbertura(data_chart=df_filter_prioridade,nome_x='prioridade_ba',nome_y='regiao')
        st.altair_chart(chart_regiao, use_container_width=True)
        #uf
        st.markdown('<p style="font-size:30px; font-weight:bold;">Prioridade e UF</p>', unsafe_allow_html=True)
        chart_uf = self.grafico_barras_prioridade_diaDaSemanaAbertura(data_chart=df_filter_prioridade,nome_x='prioridade_ba',nome_y='uf')
        st.altair_chart(chart_uf, use_container_width=True)
        #dia da semana
        st.markdown('<p style="font-size:30px; font-weight:bold;">Prioridade e dia da semana</p>', unsafe_allow_html=True)
        chart_diaSemana = self.grafico_barras_prioridade_diaDaSemanaAbertura(data_chart=df_filter_prioridade,nome_x='prioridade_ba',nome_y='nome_dia_abertura')
        st.altair_chart(chart_diaSemana, use_container_width=True)
        #descriçaõ
        st.markdown('<p style="font-size:30px; font-weight:bold;">Prioridade e descricao</p>', unsafe_allow_html=True)
        chart_descricao = self.grafico_barras_prioridade_diaDaSemanaAbertura(data_chart=df_filter_prioridade,nome_x='prioridade_ba',nome_y='breve_descr_problema')
        st.altair_chart(chart_descricao, use_container_width=True)
        #Cos
        st.markdown('<p style="font-size:30px; font-weight:bold;">Prioridade e cos</p>', unsafe_allow_html=True)
        chart_cos = self.grafico_barras_prioridade_diaDaSemanaAbertura(data_chart=df_filter_prioridade,nome_x='prioridade_ba',nome_y='Cos')
        st.altair_chart(chart_cos, use_container_width=True)
        #Est.
        st.markdown('<p style="font-size:30px; font-weight:bold;">Prioridade e estação</p>', unsafe_allow_html=True)
        chart_estacao = self.grafico_barras_prioridade_diaDaSemanaAbertura(data_chart=df_filter_prioridade,nome_x='prioridade_ba',nome_y='Est.')
        st.altair_chart(chart_estacao, use_container_width=True)
        
        
       
        st.dataframe(df_filter_prioridade, width=4000) 

       

 
def main():
    
    
    execute = Dashboard()
    execute.streamlit()
    
  
    
   

if __name__=='__main__':
    main()

    #streamlit run ponto_st.py