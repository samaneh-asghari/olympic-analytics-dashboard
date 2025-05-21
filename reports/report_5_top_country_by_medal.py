import streamlit as st
import pandas as pd
import plotly.express as px
import data_access as da

def top_country_by_medal(db:da.DataAccess):
    st.subheader("🌍 Top-Nationen nach Medaillentyp – visualisiert auf der Weltkarte")

    with st.expander("ℹ️ Worum geht es in dieser Visualisierung?"):
        st.write("""
        Diese interaktive Weltkarte zeigt die **erfolgreichsten Länder bei den Olympischen Spielen**, basierend auf der ausgewählten **Medaillenart** (Gold, Silber oder Bronze). 

        ### 🗺️ Was zeigt das Diagramm?
        **Farbskala:** Anzahl der Medaillen eines Landes – von weniger zu mehr. Die Farbverläufe reichen von **dunklem Violett → Blau → Grün → Gelb**.
        
        - Interaktive Darstellung auf einer Weltkarte  
        - Auswahloptionen:
        - Medaillentyp (Gold, Silber, Bronze)
        - Anzahl der anzuzeigenden Länder (Top 5–25)

        ### 🔍 Welche Erkenntnisse kannst du gewinnen?
        - 🥇 Welche Länder dominieren in einer bestimmten Medaillenart?
        - 🌐 Wie ist die globale Verteilung von Olympia-Erfolgen – sind sie regional konzentriert?
        - 📈 Entwicklungsmöglichkeiten: Gibt es Länder mit vielen Silber- und Bronzemedaillen, aber wenig Gold?

        Verwende die Filter unten, um verschiedene Kombinationen zu analysieren.
        """)

    left,_,right = st.columns([0.3,0.4,0.3])
    with left:
        #Nutzer kann den Medaillentyp auswählen
        select_medal=st.selectbox("Eine Medaille auswählen", ["Gold", "Silver", "Bronze"],key=9)
    with right:
        # Nutzer kann auswählen, wie viele Top-Länder angezeigt werden
        top=st.selectbox('Top',[5,10,15,20,25],1, key=89)
    
    data = db.list_top_country_by_medal(select_medal,top)

    # Erstellt eine interaktive Weltkarte (Choroplethenkarte)
    fig = px.choropleth(
        data,
        locations="Country",
        locationmode="country names",  #Plotly verwendet hier echte Ländernamen
        color="Medals",
        hover_name="Country",
        hover_data=["Medals"],
        color_continuous_scale="Viridis",
        title="Gesamtzahl der Medaillen nach Land",
      
    )
    # Layout der Karte anpassen, z.B. Hintergrundfarbe und Schriftfarbe
    fig.update_layout(
        geo=dict(
            bgcolor='#051729',  
        ),
        paper_bgcolor='#051729',
        plot_bgcolor='#051729',
        font=dict(color='white'),
    )

    # Die Karte wird im Streamlit-Dashboard in voller Containerbreite angezeigt
    st.plotly_chart(fig, use_container_width=True)