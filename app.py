import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide")   
st.image('logo.png', width= 150)

lista_anos = [2023,2024]
with st.sidebar:
    target_year = st.selectbox("Ano", lista_anos, placeholder='Escolha uma opção', index= 1)

# COMERCIAL
@st.cache_data
def get_comercial ():
    df_comercial = pd.read_excel('Indicadores_Comercial.xlsb', engine='pyxlsb')
    df_comercial = df_comercial[df_comercial['Ano'] >= 2023]
    df_comercial = df_comercial[df_comercial['Ano'] == target_year]
    df_comercial['Data Emissão'] = pd.to_numeric(df_comercial['Data Emissão'], errors='coerce')
    df_comercial['Data Emissão'] = pd.to_datetime(df_comercial['Data Emissão'], origin='1899-12-30', unit='D', errors='coerce')

    return df_comercial

df_comercial = get_comercial()

# RECURSOS HUMANOS
@st.cache_data
def get_rh():
    df_rh = pd.read_excel('Indicadores 2024 DTI.xlsx',sheet_name = 'INDICADORES 2024')
    df_rh['ABSENTEÍSMO'] = (df_rh['ABSENTEÍSMO']*100).round(2)
    df_rh['FALTAS INJUSTIFICADAS / HHT'] = (df_rh['FALTAS INJUSTIFICADAS / HHT']*100).round(2)
    return df_rh

df_rh = get_rh()

# MANUTENÇÃO
@st.cache_data
def get_manutencao():
    df_manutencao = pd.read_excel('DADOS_MANUTENÇÃO_2024.xlsx')
    df_manutencao = df_manutencao.groupby(df_manutencao['Data Abertura/Hora'].dt.month).agg(Custo = ('Custo', 'sum')).reset_index()
    return df_manutencao

df_manutencao = get_manutencao()

# NCS INTERNAS
@st.cache_data
def get_qualidade_nc_internas():
    df_qualidade_nc_internas = pd.read_excel('Indicadores da Qualidade 2024 - QUALIDADE FQ 6.2-001-01 - ELOHIM.xlsx',sheet_name = 'NC - INT. Nº DE PEÇAS')
    df_qualidade_nc_internas = df_qualidade_nc_internas.drop(0)
    new_header = df_qualidade_nc_internas.iloc[0]
    df_qualidade_nc_internas = df_qualidade_nc_internas[1:]
    df_qualidade_nc_internas.columns = new_header
    df_qualidade_nc_internas = df_qualidade_nc_internas.reset_index(drop=True)
    df_qualidade_nc_internas = df_qualidade_nc_internas.drop([12,13,14])
    df_qualidade_nc_internas['MÊS'] = pd.to_datetime(df_qualidade_nc_internas['MÊS'], format='mixed').dt.strftime('%b/%y')
    return df_qualidade_nc_internas

df_qualidade_nc_internas = get_qualidade_nc_internas()

# NCS EXTERNAS
@st.cache_data
def get_qualidade_nc_externas():
    df_qualidade_nc_externas = pd.read_excel('Indicadores da Qualidade 2024 - QUALIDADE FQ 6.2-001-01 - ELOHIM.xlsx',sheet_name = 'NC - EXT. Nº DE PEÇAS')
    df_qualidade_nc_externas = df_qualidade_nc_externas.drop(0)
    new_header = df_qualidade_nc_externas.iloc[0]
    df_qualidade_nc_externas = df_qualidade_nc_externas[1:]
    df_qualidade_nc_externas.columns = new_header
    df_qualidade_nc_externas = df_qualidade_nc_externas.reset_index(drop=True)
    df_qualidade_nc_externas = df_qualidade_nc_externas.drop([12,13,14])
    df_qualidade_nc_externas['MÊS'] = pd.to_datetime(df_qualidade_nc_externas['MÊS'], format='mixed').dt.strftime('%b/%y')
    return df_qualidade_nc_externas

df_qualidade_nc_externas = get_qualidade_nc_externas()

# CUSTO PEÇAS REFUGADAS
@st.cache_data
def get_refugo():
    df_refugo = pd.read_excel('Indicadores da Qualidade 2024 - QUALIDADE FQ 6.2-001-01 - ELOHIM.xlsx',sheet_name = 'Refugo Produto x R$')
    df_refugo.drop([0], inplace=True)
    new_header = df_refugo.iloc[0]
    df_refugo = df_refugo[1:]
    df_refugo.columns = new_header
    df_refugo.drop([14], inplace=True)
    df_refugo['Mês / Ano'] = pd.to_datetime(df_refugo['Mês / Ano'], format='mixed').dt.strftime('%b/%y')
    df_refugo.reset_index(drop=True, inplace=True)
    return df_refugo

df_refugo = get_refugo()

# CUSTO PEÇAS RETRABALHADAS
@st.cache_data
def get_retrabalho():
    df_retrabalho = pd.read_excel('Indicadores da Qualidade 2024 - QUALIDADE FQ 6.2-001-01 - ELOHIM.xlsx',sheet_name = 'Retrabalho Produto x R$')
    df_retrabalho.drop([0], inplace=True)
    new_header = df_retrabalho.iloc[0]
    df_retrabalho = df_retrabalho[1:]
    df_retrabalho.columns = new_header
    df_retrabalho.drop([14], inplace=True)
    df_retrabalho['Mês / Ano'] = pd.to_datetime(df_retrabalho['Mês / Ano'], format='mixed').dt.strftime('%b/%y')
    df_retrabalho.reset_index(drop=True, inplace=True)
    df_retrabalho.dropna(subset=['Valor (R$)'], inplace=True)
    return df_retrabalho

df_retrabalho = get_retrabalho()

# COMPARAÇÃO NÃO CONFORMIDADE EXTERNA E INTERNA
@st.cache_data
def get_comp():
    df_comp = pd.read_excel('Indicadores da Qualidade 2024 - QUALIDADE FQ 6.2-001-01 - ELOHIM.xlsx',sheet_name = 'Custo NC ')
    new_header = df_comp.iloc[0]
    df_comp = df_comp[1:]
    df_comp.columns = new_header
    df_comp.drop([13], inplace=True)
    df_comp['Mês / Ano'] = pd.to_datetime(df_comp['Mês / Ano'], format='mixed').dt.strftime('%b/%y')
    nova_linha_3 = {'Mês / Ano': 'Total', 'CUSTO DE NC EXTERNA ': df_comp['CUSTO DE NC EXTERNA '].sum(),'CUSTO DE NC INTERNA ': df_comp['CUSTO DE NC INTERNA '].sum()}
    df_comp = pd.concat([df_comp, pd.DataFrame([nova_linha_3])], ignore_index=True)
    df_comp = df_comp.reset_index(drop=True)
    df_comp_melt = pd.melt(df_comp,id_vars=['Mês / Ano'], value_vars=['CUSTO DE NC EXTERNA ', 'CUSTO DE NC INTERNA '], var_name='CUSTO',value_name='Custo (R$)')
    df_comp_melt.dropna(subset = 'Custo (R$)', inplace = True)
    df_comp_melt['Text'] = df_comp_melt['Custo (R$)'].apply(lambda x: f'R${x:.2f}')
    return df_comp_melt

df_comp_melt = get_comp()

tab1,tab2,tab3,tab4 = st.tabs(['Indicador Comercial', 'Indicador Custo', 'Indicador Recursos Humanos', 'Indicador Qualidade'])

with tab1:
    df_summary_comercial = df_comercial.groupby('Mês').agg(
        pedidos_totais = ('Status', 'count'),
        virou_pedido = ('Status', lambda x: (x == 'VIROU PEDIDO').sum())
    ).reset_index()
    df_summary_comercial['Percentual (%)'] = ((df_summary_comercial['virou_pedido']/df_summary_comercial['pedidos_totais'])*100).round(0)

    nova_linha = {'Mês':'ACM','pedidos_totais':df_summary_comercial['pedidos_totais'].sum(),'virou_pedido':df_summary_comercial['virou_pedido'].sum(),'Percentual (%)':(((df_summary_comercial['virou_pedido'].sum())/(df_summary_comercial['pedidos_totais'].sum()))*100).round(0)}
    df_summary_comercial = pd.concat([df_summary_comercial, pd.DataFrame([nova_linha])], ignore_index=True)

    month_order = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez', 'ACM']
    df_summary_comercial['Mês'] = pd.Categorical(df_summary_comercial['Mês'], categories=month_order, ordered=True)
    df_summary_comercial = df_summary_comercial.sort_values('Mês').reset_index(drop=True)
    df_summary_comercial['Percentual (%)'] = df_summary_comercial['Percentual (%)'].apply(lambda x: f"{x:.0f}%")

    fig = px.bar(df_summary_comercial, x = 'Mês', y = 'Percentual (%)', title= 'Indicador Comercial (Pedidos/Orçamentos)',text='Percentual (%)',height=500)
    fig.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)
    fig.add_shape(
    type='line',
    x0=-0.5,
    y0=35,
    x1=len(df_summary_comercial['Mês'])-0.5,
    y1=35,  
    line=dict(color='Red', width=2)
)
    fig.update_layout(title_x = 0.55, title_y = 0.95,title_xanchor = 'center',xaxis=dict(tickfont=dict(size=16)),title = dict(font=dict(size=18)))
    
    status_counts = df_comercial['Status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']

    plot_data = df_comercial.groupby(['Mês', 'Status']).size().reset_index(name='Count')
    plot_data['Mês'] = pd.Categorical(plot_data['Mês'], categories=month_order, ordered=True)
    plot_data = plot_data.sort_values('Mês').reset_index()
    fig2 = go.Figure()

    for status in plot_data['Status'].unique():
        filtered_data = plot_data[plot_data['Status'] == status]
        fig2.add_trace(
        go.Bar(
            x=filtered_data['Mês'],
            y=filtered_data['Count'],
            text=filtered_data['Count'],
            textposition='auto',
            name=status 
        )
    )

    fig2.update_layout(
        title='Balanço de Orçamentos Aprovados por Mês',
        xaxis_title='Mês',
        yaxis_title='Quantidade',
        barmode='stack' ,
        height=500
    )  
    fig2.update_layout(title_x = 0.55, title_y = 0.95,title_xanchor = 'center',xaxis=dict(tickfont=dict(size=16)),title = dict(font=dict(size=18))
                        ,legend = dict(orientation="h",
                         yanchor="top",
                         y=-0.2, 
                         xanchor="center",
                         x=0.5)
    )

    df_summary_comercial_no_ACM = df_summary_comercial.drop(df_summary_comercial[df_summary_comercial.Mês == 'ACM'].index)

    fig3 = px.bar(df_summary_comercial_no_ACM, x = 'Mês', y = 'pedidos_totais', title= 'Orçamentos Totais por Mês',text_auto='.2s',height=500)
    fig3.update_layout(title_x = 0.55, title_y = 0.95,title_xanchor = 'center',xaxis=dict(tickfont=dict(size=16)),title = dict(font=dict(size=18)))

    st.plotly_chart(fig)
    col3,col4 = st.columns(2)
    col3.plotly_chart(fig2)
    col4.plotly_chart(fig3)

with tab2:
    meses = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
         7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'}

    fat = {'Jan':1320072.98,'Fev':856599.78, 'Mar':849723.17, 'Abr':542700.38, 'Mai':1479354.77, 'Jun':1472558.7,
         'Jul':1220053.98, 'Ago':0, 'Set':0, 'Out':0, 'Nov':0, 'Dez':0}

    df_manutencao['Data Abertura/Hora'] = df_manutencao['Data Abertura/Hora'].map(meses)
    df_manutencao['Faturamento'] = df_manutencao['Data Abertura/Hora'].map(fat)
    df_manutencao['0,5% Faturamento'] = (df_manutencao['Faturamento']*0.005).round(2)
    df_manutencao['Saving'] = df_manutencao['0,5% Faturamento'] - df_manutencao['Custo']

    df_manutencao['Custo'] = df_manutencao['Custo'].round(2)

    df_manutencao['Text Custo'] = df_manutencao['Custo'].apply(lambda x: f"R${x:.0f}")
    df_manutencao['Text 0,5% Faturamento'] = df_manutencao['0,5% Faturamento'].apply(lambda x: f"R${x:.0f}")
    df_manutencao['Text Saving'] = df_manutencao['Saving'].apply(lambda x: f"R${x:.0f}")

    df_melted = df_manutencao.melt(id_vars=['Data Abertura/Hora'],
                            value_vars=['Custo', '0,5% Faturamento', 'Saving'],
                            var_name='Tipo',
                            value_name='Valor')

    df_x = df_melted.groupby('Data Abertura/Hora')['Valor'].sum()

    df_x = df_x.reset_index() 

    df_melted['Porcentagem'] = df_melted.apply(lambda row: row['Valor'] / df_x.loc[df_x['Data Abertura/Hora'] == row['Data Abertura/Hora'], 'Valor'].values[0] * 100, axis=1)
    df_melted['Porcentagem (%)'] = df_melted.apply(lambda row: f"{row['Porcentagem']:.2f}%", axis=1)

    df_melted['Text'] = df_melted.apply(lambda row: f"R${row['Valor']:.0f}", axis=1)

    fig_manu = px.bar(
        df_melted,
        x='Data Abertura/Hora',
        y='Porcentagem (%)',
        color='Tipo',
        title='Custo Manutenção Industrial',
        labels={'Valor': 'Valor (R$)', 'Tipo de Custo': 'Tipo'},
        text='Text',
        height=650
)

    fig_manu.update_layout(
        barmode='stack',
        title=dict(text='Custo Manutenção Industrial<br>Meta: Até 0,5% do Faturamento Bruto Mensal', x=0.5),
        xaxis=dict(tickangle=0),
        yaxis=dict(tickformat='R$,.2f'),
        legend_title_text='',
        legend=dict(orientation="h",
        yanchor="top",
        y=-0.2, 
        xanchor="center",
        x=0.5),
        uniformtext_minsize=8, uniformtext_mode='hide'
    )

    fig_manu.update_layout(title_x = 0.55, title_y = 0.95,title_xanchor = 'center',xaxis=dict(tickfont=dict(size=16)),title = dict(font=dict(size=18)))
    fig_manu.update_traces(textposition='outside', textfont = dict(size = 36))
    st.plotly_chart(fig_manu)

    df_refugo_total = df_refugo.drop(columns = ['Mês / Ano', 'Ideal: 1% do faturamento']).sum()
    nova_linha_2 = {'Mês / Ano': 'Total', 'Valor (R$)': df_refugo_total['Valor (R$)'], 'Ideal: 1% do faturamento': 0.0025, 'Faturamento': df_refugo_total['Faturamento'], 'Permissível (R$)':df_refugo_total['Permissível (R$)']}
    df_refugo_total = df_refugo_total.to_frame().T
    df_refugo = pd.concat([df_refugo, pd.DataFrame([nova_linha_2])], ignore_index=True)
    df_refugo['Text'] = df_refugo['Valor (R$)'].apply(lambda x: f'R${x:.2f}')
    
    df_refugo = df_refugo.dropna(subset=['Valor (R$)']).reset_index(drop=True)
    df_refugo_filtered = df_refugo.iloc[:-1]

    fig_refugo = px.bar(df_refugo, x='Mês / Ano', y='Valor (R$)', title='Custo de Peças Refugadas', text='Text',height=650)
    fig_refugo.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)
    fig_refugo.update_layout(title_x = 0.55, title_y = 0.95,title_xanchor = 'center',xaxis=dict(tickfont=dict(size=16)),title = dict(font=dict(size=18)))
    fig_refugo.add_trace(go.Scatter(x=df_refugo_filtered['Mês / Ano'], y= df_refugo_filtered['Permissível (R$)'],
                                    mode='lines+markers+text', 
                                    line=dict(color='red', width=2),
                                    textposition="top left",
                                    textfont=dict(size=16),
                                    name = 'Permissível',
                                    text=[f"R$ {v:.2f}".replace('.', ',') for v in df_refugo_filtered['Permissível (R$)']]))
    fig_refugo.update_layout(legend=dict(orientation="h",
        yanchor="top",
        y=-0.2, 
        xanchor="center",
        x=0.5, font = dict(size=16)))
    
    df_retrabalho_total = df_retrabalho.drop(columns = ['Mês / Ano', 'Ideal: 1% do faturamento']).sum()
    nova_linha_3 = {'Mês / Ano': 'Total', 'Valor (R$)': df_retrabalho_total['Valor (R$)'], 'Ideal: 1% do faturamento': 0.005, 'Faturamento': df_retrabalho_total['Faturamento'], 'Permissível (R$)':df_retrabalho_total['Permissível (R$)']}
    df_retrabalho_total = df_retrabalho_total.to_frame().T
    df_retrabalho = pd.concat([df_retrabalho, pd.DataFrame([nova_linha_3])], ignore_index=True)

    df_retrabalho['Text'] = df_retrabalho['Valor (R$)'].apply(lambda x: f'R${x:.2f}')
    df_retrabalho_filtered = df_retrabalho.iloc[:-1]

    fig_retrabalho = px.bar(df_retrabalho, x='Mês / Ano', y='Valor (R$)', title='Custo de Peças Retrabalhadas', text='Text',height=650)
    fig_retrabalho.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)
    fig_retrabalho.update_layout(title_x = 0.55, title_y = 0.95,title_xanchor = 'center',xaxis=dict(tickfont=dict(size=16)),title = dict(font=dict(size=18)))
    fig_retrabalho.add_trace(go.Scatter(x=df_retrabalho_filtered['Mês / Ano'], y= df_retrabalho_filtered['Permissível (R$)'],
                                    mode='lines+markers+text', 
                                    line=dict(color='red', width=2),
                                    textposition="top left",
                                    textfont=dict(size=16),
                                    name= 'Permissível',
                                    text=[f"R$ {v:.2f}".replace('.', ',') for v in df_retrabalho_filtered['Permissível (R$)']]))
    fig_retrabalho.update_layout(legend=dict(orientation="h",
        yanchor="top",
        y=-0.2, 
        xanchor="center",
        x=0.5,font = dict(size=16)))
    
    fig_comp = px.bar(df_comp_melt, x="Mês / Ano", y="Custo (R$)", color='CUSTO', barmode='group',title = 'Comparação Custo de Não Conformidade', text='Text')
    fig_comp.update_layout(yaxis_title='Custo (R$)',title_x = 0.55, title_y = 0.95,title_xanchor = 'center',xaxis=dict(tickfont=dict(size=18)),yaxis=dict(tickfont=dict(size=18)),title = dict(font=dict(size=18)),legend=dict(orientation="h",
        yanchor="top",
        y=-0.2, 
        xanchor="center",
        x=0.5,font = dict(size=14)))
    fig_comp.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)

    st.plotly_chart(fig_refugo)
    st.plotly_chart(fig_retrabalho)
    st.plotly_chart(fig_comp)

with tab3:
    df_rh['ABSENTEISMO_TEXT'] = df_rh['ABSENTEÍSMO'].apply(lambda x: f"{x:.2f}%")
    fig_just = px.bar(df_rh,x='MÊS',y='ABSENTEÍSMO', title='FALTAS JUSTIFICADAS/HHT',text='ABSENTEISMO_TEXT')
    fig_just.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)
    fig_just.add_annotation(
        text="META: ABAIXO DE 2,0%",
        xref="paper", yref="paper",
        x=0.5, y=1.15, showarrow=False,
        font=dict(size=14)
    )
    fig_just.add_shape(
        type='line',
        x0=-0.5,
        y0=2,
        x1=12,
        y1=2,
        line=dict(color='Red', width=2)
    )
    fig_just.update_layout(title_x = 0.55, title_y = 0.95,title_xanchor = 'center',xaxis=dict(tickfont=dict(size=16)),title = dict(font=dict(size=18)))

    df_rh['FALTAS INJUSTIFICADAS_TEXT'] = df_rh['FALTAS INJUSTIFICADAS / HHT'].apply(lambda x: f"{x:.2f}%")
    fig_injust = px.bar(df_rh,x='MÊS',y='FALTAS INJUSTIFICADAS / HHT', title='FALTAS INJUSTIFICADAS/HHT',text = 'FALTAS INJUSTIFICADAS_TEXT')
    fig_injust.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)
    fig_injust.add_annotation(
        text="META: ABAIXO DE 1,5%",
        xref="paper", yref="paper",
        x=0.5, y=1.15, showarrow=False,
        font=dict(size=14)
    )
    fig_injust.add_shape(
        type='line',
        x0=-0.5,
        y0=1.5,
        x1=12,
        y1=1.5,
        line=dict(color='Red', width=2)
    )
    fig_injust.update_layout(title_x = 0.55, title_y = 0.95,title_xanchor = 'center',xaxis=dict(tickfont=dict(size=16)),title = dict(font=dict(size=18)))

    df_rh['HORAS DE TREINAMENTO / HHT'] = df_rh['HORAS DE TREINAMENTO / HHT']*100
    df_rh['TREINAMENTOS_TEXT'] = df_rh['HORAS DE TREINAMENTO / HHT'].apply(lambda x: f"{x:.2f}%")
    fig_treina = px.bar(df_rh,x='MÊS',y='HORAS DE TREINAMENTO / HHT', title='TREINAMENTOS/HHT',text = 'TREINAMENTOS_TEXT')
    fig_treina.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)
    fig_treina.add_annotation(
        text="META: ABAIXO DE 1,5%",
        xref="paper", yref="paper",
        x=0.5, y=1.15, showarrow=False,
        font=dict(size=14)
    )
    fig_treina.add_shape(
        type='line',
        x0=-0.5,
        y0=1.5,
        x1=12,
        y1=1.5,
        line=dict(color='Red', width=2)
    )
    fig_treina.update_layout(title_x = 0.55, title_y = 0.95,title_xanchor = 'center',xaxis=dict(tickfont=dict(size=16)),title = dict(font=dict(size=18)))

    df_rh['HORAS EXTRAS / HHT'] = df_rh['HORAS EXTRAS / HHT']*100
    df_rh['HORAS_EXTRAS_TEXT'] = df_rh['HORAS EXTRAS / HHT'].apply(lambda x: f"{x:.2f}%")
    fig_hora_ext = px.bar(df_rh,x='MÊS',y='HORAS EXTRAS / HHT', title='HORAS EXTRAS/HHT',text = 'HORAS_EXTRAS_TEXT')
    fig_hora_ext.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)
    fig_hora_ext.add_annotation(
        text="META: ABAIXO DE 10%",
        xref="paper", yref="paper",
        x=0.5, y=1.15, showarrow=False,
        font=dict(size=14)
    )
    fig_hora_ext.add_shape(
        type='line',
        x0=-0.5,
        y0=10,
        x1=12   ,
        y1=10,
        line=dict(color='Red', width=2)
    )
    fig_hora_ext.update_layout(title_x = 0.55, title_y = 0.95,title_xanchor = 'center',xaxis=dict(tickfont=dict(size=16)),title = dict(font=dict(size=18)))

    col5,col6 = st.columns(2)
    col7,col8 = st.columns(2)

    col5.plotly_chart(fig_just)
    col6.plotly_chart(fig_injust)
    col7.plotly_chart(fig_treina)
    col8.plotly_chart(fig_hora_ext)

with tab4:
    df_qualidade_nc_internas = df_qualidade_nc_internas.dropna(subset='Qtde. NC Disposição')
    df_qualidade_nc_internas['Qtde. NC Disposição'] = df_qualidade_nc_internas['Qtde. NC Disposição'] * 100
    df_qualidade_nc_internas['Qtde. NC Disposição_T'] = df_qualidade_nc_internas['Qtde. NC Disposição'].apply(lambda x: f"{x:.1f}%")

    fig_ind_nc_int = px.bar(df_qualidade_nc_internas, x='MÊS', y='Qtde. NC Disposição', title='Índice de Não Conformidades Internas', text='Qtde. NC Disposição_T', height=650)
    fig_ind_nc_int.update_layout(title_x = 0.55,yaxis_title='%', title_y = 0.95,title_xanchor = 'center',xaxis=dict(tickfont=dict(size=16)),title = dict(text='Índice de Não Conformidades Internas<br>Meta: Abaixo de 1% - Máximo de 1 Peça NC em 100 Peças Fabricadas',font=dict(size=18)))
    fig_ind_nc_int.add_shape(
            type='line',
            x0=-0.5,
            y0=1,
            x1=len(df_qualidade_nc_internas['MÊS'])-0.5,
            y1=1,
            line=dict(color='Red', width=2))
    fig_ind_nc_int.update_traces(textposition='outside',textfont=dict(size=18))

    st.plotly_chart(fig_ind_nc_int)
    
    totais_por_processo = df_qualidade_nc_internas.drop(columns='MÊS').sum()
    df_totais = totais_por_processo.reset_index()
    df_totais.columns = ['Processo', 'Total']
    df_totais= df_totais.drop([21,22,23,24])
    df_totais_drop_1= df_totais.drop([20])
    total_nc_internas = df_totais_drop_1['Total'].sum()
    df_totais['Porcentagem'] = (df_totais['Total']/total_nc_internas)*100
    df_totais['Porcentagem (%)'] = df_totais['Porcentagem'].apply(lambda x: f"{x:.2f}%")

    fig_total_processo = px.bar(df_totais, x='Processo', y='Porcentagem (%)', title="Total Acumulado/Total de NC's Internas", text='Total',height=650)
    fig_total_processo.update_layout(title_x = 0.55, title_y = 0.95,title_xanchor = 'center',xaxis=dict(tickfont=dict(size=16)),title = dict(text= "Total de NC's Internas - Anual por Setor",font=dict(size=18)),legend = dict(orientation="h",yanchor="top",y=-0.2,xanchor="center",x=0.5))
    fig_total_processo.update_traces(
    textposition='outside',
    textfont=dict(size=18))

    st.plotly_chart(fig_total_processo)
    
    df_qualidade_nc_externas = df_qualidade_nc_externas.dropna(subset='Qtde. NC Disposição')

    df_qualidade_nc_externas['Qtde. NC Disposição'] = df_qualidade_nc_externas['Qtde. NC Disposição']*100
    df_qualidade_nc_externas['Qtde. NC Disposição_T'] = df_qualidade_nc_externas['Qtde. NC Disposição'].apply(lambda x: f"{x:.2f}%")
    fig_ind_nc_ext = px.bar(df_qualidade_nc_externas, x='MÊS', y='Qtde. NC Disposição', title='Índice de Não Conformidades Externas', text='Qtde. NC Disposição_T', height=650)
    fig_ind_nc_ext.update_layout(title_x = 0.55,yaxis_title='%', title_y = 0.95,title_xanchor = 'center',xaxis=dict(tickfont=dict(size=16)),title = dict(text="Índice de Não Conformidades Externas<br>Meta: Abaixo de 0,5% - Máximo de 5 Peças NC em 1000 Peças Fabricadas",font=dict(size=18)),legend = dict(orientation="h",yanchor="top",y=-0.2,xanchor="center",x=0.5))
    fig_ind_nc_ext.add_shape(
            type='line',
            x0=-0.5,
            y0=0.5,
            x1= len(df_qualidade_nc_externas['MÊS'])-.05,
            y1=0.5,
            line=dict(color='Red', width=2))
    fig_ind_nc_ext.update_traces(
    textposition='outside',
    textfont=dict(size=18)
)
    st.plotly_chart(fig_ind_nc_ext)

    totais_por_empresa = df_qualidade_nc_externas.drop(columns='MÊS').sum()
    df_totais_empresas = totais_por_empresa.reset_index()
    df_totais_empresas.columns = ['Empresa', 'Total']
    df_totais_empresas= df_totais_empresas.drop([12,13,14,15])
    df_totais_empresas_drop_1= df_totais_empresas.drop([11])
    total_nc_externas = df_totais_empresas_drop_1['Total'].sum()
    df_totais_empresas['Porcentagem'] = (df_totais_empresas['Total']/total_nc_externas)*100
    df_totais_empresas['Porcentagem (%)'] = df_totais_empresas['Porcentagem'].apply(lambda x: f"{x:.2f}%")

    fig_total_empresa = px.bar(df_totais_empresas, x='Empresa', y='Porcentagem (%)', title="Total Acumulado/ Total de NC's Externas", text='Total', height=650)
    fig_total_empresa.update_layout(title_x = 0.55, title_y = 0.95,title_xanchor = 'center',xaxis=dict(tickfont=dict(size=16)),title = dict(text="Quantidade de NC's Externa - Anual por Cliente (Em n° de Peças)",font=dict(size=18)),legend = dict(orientation="h",yanchor="top",y=-0.2,xanchor="center",x=0.5))
    fig_total_empresa.update_traces(
    textposition='outside',
    textfont=dict(size=18)
)
    st.plotly_chart(fig_total_empresa)
