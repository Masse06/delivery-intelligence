import streamlit as st
import pandas as pd
import requests
import altair as alt

def fetch_data():
    api_url = "http://localhost:8080/api/v1/analytics/profitability"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error conectando con el backend Java: {e}")
        return []

def build_dashboard():
    # Configuracion de la pagina
    st.set_page_config(page_title="Delivery Intelligence", layout="wide")
    
    st.title("Delivery Intelligence Engine")
    st.markdown("### Motor Analitico de Rentabilidad y Propinas")
    
    raw_data = fetch_data()
    
    if not raw_data:
        st.warning("No hay datos disponibles. Asegurate de que Spring Boot esta corriendo.")
        return

    df = pd.DataFrame(raw_data)
    
    # KPIs Globales
    st.markdown("#### Indicadores Globales de Negocio")
    col_total, col_zona, col_hora = st.columns(3)
    
    top_zone = df.loc[df['avgTipPercentage'].idxmax()]
    avg_global_tip = df['avgTipPercentage'].mean()
    
    with col_total:
        st.metric(
            label="Total Pedidos Analizados", 
            value=f"{df['totalOrders'].sum()} pedidos",
            delta="Base de datos de produccion"
        )
    with col_zona:
        st.metric(
            label="Zona Mas Rentable", 
            value=f"{top_zone['zoneAlias']}", 
            delta=f"{top_zone['avgTipPercentage']}% (Media global: {avg_global_tip:.1f}%)"
        )
    with col_hora:
        st.metric(
            label="Franja Horaria Destacada", 
            value=f"{top_zone['timeSlot'].upper()}", 
            delta="Horario recomendado"
        )

    st.divider()

    # Ranking Principal
    st.markdown("#### Ranking de Zonas con Mayor Margen")
    
    top_ranking_df = df.groupby('zoneAlias')['avgTipPercentage'].mean().reset_index()
    top_ranking_df = top_ranking_df.sort_values('avgTipPercentage', ascending=False).head(10)
    
    bar_chart = alt.Chart(top_ranking_df).mark_bar(cornerRadiusTopRight=5, cornerRadiusBottomRight=5).encode(
        x=alt.X('avgTipPercentage:Q', title='Porcentaje de Propina Medio'),
        y=alt.Y('zoneAlias:O', sort='-x', title='Zona Analitica'),
        color=alt.Color('avgTipPercentage:Q', scale=alt.Scale(scheme='blues'), legend=None),
        tooltip=['zoneAlias', 'avgTipPercentage']
    ).properties(height=350)
    
    st.altair_chart(bar_chart, use_container_width=True)

    st.divider()

    # Distribucion General
    st.markdown("#### Distribucion Completa de Rentabilidad")
    
    # Calculo algoritmico de la altura del grafico
    num_zonas = len(df['zoneAlias'].unique())
    altura_dinamica = max(400, num_zonas * 25) 
    
    heatmap = alt.Chart(df).mark_rect(cornerRadius=3).encode(
        x=alt.X('timeSlot:O', title='Franja Horaria', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('zoneAlias:O', title='Zona Analitica', sort='-x'),
        color=alt.Color('avgTipPercentage:Q', scale=alt.Scale(scheme='greens'), title='Margen Propina'),
        tooltip=['zoneAlias', 'timeSlot', 'avgTipPercentage', 'totalOrders']
    ).properties(
        height=altura_dinamica
    )
    
    st.altair_chart(heatmap, use_container_width=True)

if __name__ == "__main__":
    build_dashboard()