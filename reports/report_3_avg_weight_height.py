import streamlit as st
import pandas as pd
import plotly.express as px
import data_access as da

def report_avg_height_weight(db:da.DataAccess):

    st.subheader("📏 Körpermaße erfolgreicher Athlet:innen nach Sportart & Geschlecht")

    with st.expander("ℹ️ Worum geht es in dieser Visualisierung?"):
        st.write("""
        Dieses Diagramm zeigt die **durchschnittliche Körpergröße und das Gewicht** von Athlet:innen, die bei den Olympischen Spielen **eine Medaille gewonnen** haben – aufgeschlüsselt nach **Sportart und Geschlecht**.

        ### 📊 Was zeigt das Diagramm?
        Es handelt sich um ein **Streudiagramm**, in dem jeder Punkt eine Kombination aus Sportart und Geschlecht darstellt. Die Achsen zeigen:
        - **x-Achse**: Durchschnittliches Gewicht (kg)
        - **y-Achse**: Durchschnittliche Körpergröße (cm)
        - **Farbe**: Sportart
        - **Symbol**: Geschlecht (♀/♂)
        - **Größe des Punktes**: Anzahl der erfassten Medaillengewinner:innen

        ### 🔍 Erkenntnisse, die du aus dem Diagramm gewinnen kannst:
        - 📐 Welche Sportarten besonders große oder schwere Athlet:innen erfordern
        - ⚖️ Ob es Unterschiede in den Körpermaßen zwischen Männern und Frauen innerhalb einer Sportart gibt
        - 🏋️‍♂️ Welche Sportarten eine große Anzahl erfolgreicher Athlet:innen aufweisen
        - 🔍 Körperliche Gemeinsamkeiten von Medaillengewinner:innen in bestimmten Disziplinen
        - 🌍 Wie sich Sportarten hinsichtlich der körperlichen Anforderungen unterscheiden
        - 🎯 Nützlich zur Talentförderung & Spezialisierung – welche Körpermaße passen zu welchen Sportarten?

        Nutze die Filter unten, um gezielt Sportarten und Geschlechter auszuwählen und Unterschiede besser zu analysieren.
        """)

    #Holt alle Sportarten aus der Datenbank.    
    all_sports = db.list_sports()
    #Fügt "Alle" als Auswahloption hinzu.
    all_sports.insert(0,"Alle")

    #Multiselect-Filter: Standardmäßig  "Alle" vorausgewählt.
    selected_sports = st.multiselect("Sportart(en) auswählen", all_sports, default=all_sports[:1],key=5) 
    if "Alle" in selected_sports:
        selected_sports=all_sports


    left,_ = st.columns([0.2,0.8])
    with left:
        #Filter für Geschlecht
        selected_sex = st.selectbox("Geschlecht", ['Mann','Frau','Alle'], 2)

        if selected_sex=='Mann':
            selected_sex = ['M']
        elif selected_sex == 'Frau':
            selected_sex = ['F']
        else:
            selected_sex = ['F','M']

    #Datenabruf
    result = db.list_avg_weight_height(selected_sports,selected_sex)
    
    #Erstellt ein interaktives Streudiagramm
    fig = px.scatter(
        result,
        x="avg_weight",
        y="avg_height",
        color="Sport",
        symbol="Sex",
        hover_name="Sport",
        size="athlete_count",
        title="Durchschnittliche Körpergröße vs. Gewicht von medaillengewinnenden Athleten",
        labels={
            "avg_height": "Durchschnittliche Körpergröße (cm)",
            "avg_weight": "Durchschnittliches Gewicht (kg)"
        }
    )

    st.plotly_chart(fig)