import streamlit as st
import pandas as pd
import plotly.express as px

# Configurar o layout da página
st.set_page_config(
    page_title="Análise de Aluguel de Imóveis", 
    page_icon="ico-aluguel.png",
    layout="wide"
)

# Função para carregar dados com cache
def ler_dados():
    df = pd.read_csv("houses_to_rent_v2.csv")
    df['animal'] = df['animal'].replace({'acept': 'Sim', 'not acept': 'Não'})
    df['city'] = df['city'].astype(str)
    
    # Garantir que a coluna 'area' é numérica e filtrar valores nulos
    df['area'] = pd.to_numeric(df['area'], errors='coerce')
    df = df.dropna(subset=['area'])
    
    return df


# Função para aplicar filtros
def aplicar_filtros(df):
    st.subheader("Filtros para Análise")
    
    # Criação de 3 colunas para organizar os filtros lado a lado
    col1, col2, col3 = st.columns(3)

    # Filtros para cidades
    with col1:
        cities = st.multiselect(
            "Selecione as Cidades", 
            options=sorted(df["city"].unique()), 
            default=sorted(df["city"].unique())
        )

    # Filtro para intervalo de área
    with col2:
        area_min, area_max = st.slider(
            "Selecione o intervalo de área (m²)", 
            int(df["area"].min()), int(df["area"].max()), 
            (int(df["area"].min()), int(df["area"].max()))
        )
    
    # Filtro para intervalo de aluguel
    with col3:
        rent_min, rent_max = st.slider(
            "Selecione o intervalo de aluguel (R$)", 
            int(df["rent amount (R$)"].min()), int(df["rent amount (R$)"].max()), 
            (int(df["rent amount (R$)"].min()), int(df["rent amount (R$)"].max()))
        )
    
    # Criação de mais 2 colunas para os outros filtros
    col4, col5 = st.columns(2)
    
    # Filtro para aceitar animais
    with col4:
        animal_filter = st.multiselect(
            "Permitir animais de estimação?", 
            options=["Sim", "Não"], 
            default=["Sim", "Não"]
        )
    
    # Filtro para quantidade de quartos
    with col5:
        room_filter = st.multiselect(
            "Selecione a quantidade de quartos", 
            options=sorted(df["rooms"].unique()), 
            default=sorted(df["rooms"].unique())
        )

    return df[
        (df['city'].isin(cities)) & 
        (df['area'] >= area_min) &
        (df['rent amount (R$)'] >= rent_min) & 
        (df['rent amount (R$)'] <= rent_max) &
        (df['animal'].isin(animal_filter)) & 
        (df['rooms'].isin(room_filter))
    ]


# Função para gerar o gráfico de quantidade de casas por cidade
def plotar_contagem_cidades(data_frame_filtrado):
    city_count = data_frame_filtrado['city'].value_counts().reset_index()
    city_count.columns = ['city', 'house_count']
    city_count = city_count.sort_values(by='house_count', ascending=False)
    
    fig_cities = px.bar(
        city_count, x='city', y='house_count', text='house_count', color='house_count',
        title="Quantidade de Casas por Cidade", 
        color_continuous_scale=[(0.0, '#87CEEB'), (1.0, '#6A5ACD')], 
        labels={'city': 'Cidade', 'house_count': 'Quantidade de Casas'}
    )
    fig_cities.update_traces(textposition='outside', marker_line_width=0)
    fig_cities.update_layout(
        margin=dict(l=0, r=0, t=50, b=0), 
        coloraxis_showscale=False, yaxis=dict(showticklabels=False), 
        title_font=dict(size=18, color='#333333'), 
        showlegend=False, 
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(245, 245, 245, 1)'
    )
    return fig_cities

# Função para gerar o gráfico de aluguel por quantidade de quartos e cidade
def plotar_preço_por_quartos_cidade(data_frame_filtrado):
    price_by_rooms_city = data_frame_filtrado.groupby(['rooms', 'city'])['rent amount (R$)'].mean().reset_index()
    
    fig_price_rooms_city = px.bar(
        price_by_rooms_city, 
        x='rooms', y='rent amount (R$)', color='city', barmode='group', 
        labels={'rooms': 'Quantidade de Quartos', 'rent amount (R$)': 'Aluguel Médio (R$)'}, 
        title="Preço Médio de Aluguel por Quantidade de Quartos e Cidade", 
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_price_rooms_city.update_layout(
        margin=dict(l=100, r=0, t=50, b=0), 
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(245, 245, 245, 1)', 
        xaxis_title="Quantidade de Quartos", yaxis_title="Aluguel Médio (R$)", 
        legend_title="Cidade", 
        font=dict(size=14), 
        title_font=dict(size=18, color='#333333'), 
        showlegend=True
    )
    return fig_price_rooms_city

# Função para gerar o gráfico de média de área por cidade
def plotar_area_por_cidade(data_frame_filtrado):
    city_mean = data_frame_filtrado.groupby('city').agg({'area': 'mean'}).reset_index()
    city_mean['formatted_area'] = city_mean['area'].apply(lambda x: f'{x:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."))

    fig_area = px.bar(
        city_mean, x='area', y='city', text='formatted_area', color='area',
        color_continuous_scale=[(0.0, '#87CEEB'), (1.0, '#6A5ACD')], 
        title="Média de Área por Cidade", labels={'city': 'Cidade', 'area': 'Área Média (m²)'}
    )
    fig_area.update_traces(textposition='outside', marker_line_width=0)
    fig_area.update_layout(
        margin=dict(l=0, r=0, t=50, b=0), 
        coloraxis_showscale=False, yaxis=dict(showticklabels=True), 
        title_font=dict(size=18, color='#333333'), 
        showlegend=False, 
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(245, 245, 245, 1)'
    )
    return fig_area

# Função para gerar o gráfico de média de aluguel por cidade
def plotar_aluguel_por_cidade(data_frame_filtrado):
    city_mean = data_frame_filtrado.groupby('city').agg({'rent amount (R$)': 'mean'}).reset_index()
    city_mean['formatted_rent'] = city_mean['rent amount (R$)'].apply(lambda x: f'R$ {x:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."))

    fig_rent = px.line(
        city_mean, x='city', y='rent amount (R$)', text='formatted_rent', markers=True, 
        title="Média de Aluguel por Cidade", 
        labels={'city': 'Cidade', 'rent amount (R$)': 'Aluguel Médio (R$)'}
    )
    fig_rent.update_traces(
        textposition='top center', line=dict(width=3), marker=dict(size=10, color='red')
    )
    fig_rent.update_layout(
        margin=dict(l=0, r=0, t=50, b=0), 
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(245, 245, 245, 1)', 
        xaxis_title=None, yaxis_title="Aluguel Médio (R$)", 
        title_font=dict(size=18, color='#333333'), 
        showlegend=False
    )
    return fig_rent

# Função para gerar o gráfico de pizza de proporção de animais
def plotar_pizza_animais(data_frame_filtrado):
    animal_proportion = data_frame_filtrado['animal'].value_counts().reset_index()
    animal_proportion.columns = ['Permissão de Animais', 'Contagem']

    fig_animal_pie = px.pie(
        animal_proportion, names='Permissão de Animais', values='Contagem', 
        title='Proporção de Casas que Aceitam Animais', 
        color_discrete_sequence=px.colors.qualitative.Pastel,
        labels={'Permissão de Animais': 'Aceita Animais?', 'Contagem': 'Contagem'},
        width=200, height=400
    )
    fig_animal_pie.update_layout(
        title_font=dict(size=18, color='#333333'), 
        paper_bgcolor='rgba(245, 245, 245, 1)', 
        margin=dict(l=0, r=0, t=50, b=0)
    )
    return fig_animal_pie

# Função para gerar o gráfico de violino para a distribuição de valores
def plotar_distribuição_aluguel(data_frame_filtrado):
    # Retirar os outliers
    data_frame_filtrado = remove_outliers(data_frame_filtrado, 'total (R$)')

    # Gráfico de Distribuição dos Valores Embutidos no Aluguel por Cidade
    fig_rent_distribution = px.violin(
        data_frame_filtrado, 
        y='rent amount (R$)', 
        box=True, 
        points='all', 
        title='Distribuição de Aluguel com Box e Pontos', 
        color='city',
        labels={'rent amount (R$)': 'Aluguel (R$)'}
    )
    fig_rent_distribution.update_layout(
        title_font=dict(size=18, color='#333333'), 
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(245, 245, 245, 1)', 
        margin=dict(l=0, r=0, t=50, b=0)
    )
    return fig_rent_distribution

# Função para remover outliers
def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

# Função principal para renderizar o dashboard
def main():
    # Carregar a base de dados
    df = ler_dados()

    # Título do dashboard
    st.title("Análise de Aluguel")

    # Aplicar filtros aos dados
    data_frame_filtrado = aplicar_filtros(df)

    # Verificar se há dados filtrados
    if not data_frame_filtrado.empty:
        col1, col2 = st.columns(2)
        
        # Exibir gráficos
        with col1:
            st.plotly_chart(plotar_contagem_cidades(data_frame_filtrado), use_container_width=True)
        
        with col2:
            st.plotly_chart(plotar_preço_por_quartos_cidade(data_frame_filtrado), use_container_width=True)

        col2, col3, col4 = st.columns(3)
        
        with col2:
            st.plotly_chart(plotar_area_por_cidade(data_frame_filtrado), use_container_width=True)

        with col3:
            st.plotly_chart(plotar_aluguel_por_cidade(data_frame_filtrado), use_container_width=True)
        
        with col4:
            st.plotly_chart(plotar_pizza_animais(data_frame_filtrado), use_container_width=True)
            
        st.plotly_chart(plotar_distribuição_aluguel(data_frame_filtrado), use_container_width=True)
    else:
        st.write("Nenhum dado disponível com os filtros aplicados.")

# Executar a função principal
if __name__ == "__main__":
    main()
