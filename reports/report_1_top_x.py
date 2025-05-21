import streamlit as st
import pandas as pd
import plotly.express as px
import data_access as da

def list_top_countries_by_total(db:da.DataAccess):

    #Überschrift
    st.subheader("🏅 Top-Länder nach olympischer Medaillenzahl (filterbar nach Jahr & Sport)")
    
    # Erklärung für Nutzer im aufklappbaren Bereich (Expander): Was zeigt das Diagramm?

    with st.expander("ℹ️ Was zeigt dieses Diagramm? (Zum Aufklappen klicken)"):
        st.write("""
            Dieses Diagramm visualisiert die **erfolgreichsten Länder** bei den Olympischen Spielen in Bezug auf die **insgesamt gewonnenen Medaillen** – innerhalb eines frei wählbaren Zeitraums und bestimmter Sportarten.

            ### 📊 Was zeigt das Diagramm?
            Es zeigt ein **gestapeltes Balkendiagramm**, in dem Länder nach der **Gesamtzahl ihrer Medaillen (Gold, Silber, Bronze)** sortiert sind. Die Daten lassen sich filtern nach:

            - 📆 Jahresbereich (z. B. 1960 bis 2016)
            - 🏋️ Ausgewählte Sportarten (z. B. Leichtathletik, Schwimmen)
            - 🔢 Anzahl der Top-Länder (z. B. Top 10, Top 20)

            ### 🔍 Was lässt sich aus dem Diagramm ableiten?
            - 🥇 Welche Länder im gewählten Zeitraum insgesamt die meisten Medaillen gewonnen haben
            - 🥈 Wie sich die Medaillentypen (Gold, Silber, Bronze) je Land verteilen
            - 🏅 Welche Sportarten besonders zur Medaillenausbeute einzelner Länder beitragen
            - 🎯 Länder, die sich auf bestimmte Medaillentypen spezialisiert haben (z. B. viele Gold- oder Bronzemedaillen)

            ➡️ Nutze die Filter unten, um spannende Trends in der olympischen Leistung verschiedener Nationen zu entdecken und zu analysieren!

        """)


    rangecol,_,topcol=st.columns([0.6,0.2, 0.2])
    with rangecol:
        #Slider für Jahresauswahl
        start_year, end_year = st.slider("Jahresbereich auswählen", 1904, 2016, (1960, 2016), step=4)
    with topcol:
        #Auswahl der Anzahl Top-Länder
        top=st.selectbox('Top',[5,10,15,20,25],1)

    all_sports = db.list_sports()
    all_sports.insert(0,"Alle")

    selected_sports = st.multiselect("Sportart(en) auswählen", all_sports, default=all_sports[:1]) 
    if "Alle" in selected_sports:
        selected_sports=all_sports    


    # Fetch data
    df = db.list_top_countries_by_total_medal(limit=top,from_year=start_year,to_year=end_year, sports=selected_sports) 
    
    #Wandelt das DataFrame von Wide- in Long-Format um, damit Medaillentypen gestapelt dargestellt werden können
    long_df = df.melt(
        id_vars = ["Country","Gesamtmedaillen"],
        value_vars = ["Goldmedaillen", "Silbermedaillen", "Bronzemedaillen"],
        var_name = "Medaille",
        value_name = "Anzahl"
    )

    # Diagramm erstellen: Gestapeltes Balkendiagramm mit Plotly Express
    fig = px.bar(
        long_df,
        x="Country",
        y="Anzahl",
        color="Medaille",
        title=f"Top {top} Länder nach Medaillen ({start_year}–{end_year})",
        hover_data={
                "Country": False,
                "Gesamtmedaillen": True,
                "Anzahl": True,
                "Medaille": True
            },
        barmode="stack",
        color_discrete_map={
            "Goldmedaillen": "#FFD700",    
            "Silbermedaillen": "#C0C0C0",  
            "Bronzemedaillen": "#CD7F32"   
        },
    )
    # Zeigt das Diagramm im Streamlit-Dashboard
    st.plotly_chart(fig)