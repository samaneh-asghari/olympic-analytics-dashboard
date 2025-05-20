import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import data_access as da

def gender_teilnehmen_medal(db:da.DataAccess):

    st.subheader("🏃‍♂️ Olympiateilnahmen & Medaillengewinne nach Geschlecht im Zeitverlauf")

    with st.expander("ℹ️ Was zeigt dieses Diagramm? (Zum Aufklappen klicken)"):
        st.write("""
        Dieses Diagramm zeigt die Entwicklung der **Teilnehmerzahlen und Medaillengewinne** bei den Olympischen Spielen über die Jahre – getrennt nach **Geschlecht** und **Zeitraum**.

        ### 📊 Was wird visualisiert?
        - **Gestapelte Balken** zeigen die Anzahl gewonnener **Gold-, Silber- und Bronzemedaillen** pro Jahr.
        - Eine **zusätzliche Linie** zeigt die **Anzahl der teilnehmenden Athlet:innen** im jeweiligen Jahr.
        - Die Daten sind **filterbar nach Geschlecht** (Mann oder Frau) und **Jahresbereich** (z. B. 1960–2016).

        ### 🔍 Erkenntnisse, die der User aus dem Diagramm gewinnen kann:
        - 🥇 Wie sich die **Medaillengewinne eines Geschlechts** im Zeitverlauf entwickelt haben.
        - 👥 Wie viele **Athlet:innen eines Geschlechts** an den Spielen teilgenommen haben.
        - 📈 Gibt es eine **Korrelation zwischen Teilnehmerzahl und Medaillenerfolg**?
        - ⚖️ Haben sich **geschlechtsspezifische Unterschiede** im Medaillengewinn über die Jahre verringert oder verstärkt?
        - 🧭 In welchen Jahren war die Teilnahme besonders hoch oder niedrig .
        

         Nutze die Filter unten , um gezielt Trends, Entwicklungen und Unterschiede zwischen Männern und Frauen im olympischen Wettbewerb zu analysieren!
        """)
    
    #Erstellt zwei Spalten für Filter. Die mittlere Spalte (_) bleibt leer als Abstandhalter.
    rangecol,_,gendercol=st.columns([0.6,0.2, 0.2])
    with rangecol:
        #Ein Jahrbereichs-Slider, Standard: 1960–2016.
        start_year, end_year = st.slider("Jahresbereich auswählen", 1904, 2016, (1960, 2016), step=4, key='part')
    with gendercol:
        #Auswahlbox für Geschlecht.
        gender=st.selectbox('Geschlecht',['Mann','Frau'],1,)
        if gender == 'Mann':
            gender = 'M'
        else:
            gender = 'F'

    df = db.list_teilnehmen_medal_by_gender(from_year=start_year, to_year=end_year,gender=gender)


    fig = go.Figure()

    # Stacked bars for medals
    fig.add_trace(go.Bar(
        x=df["Year"],
        y=df["num_gold"],
        name="Gold Medals",
        marker_color="gold"
    ))
    fig.add_trace(go.Bar(
        x=df["Year"],
        y=df["num_silver"],
        name="Silver Medals",
        marker_color="silver"
    ))
    fig.add_trace(go.Bar(
        x=df["Year"],
        y=df["num_bronze"],
        name="Bronze Medals",
        marker_color="#cd7f32"  # bronze color
    ))

    # Fügt eine Linie
    #yaxis="y2": Zweite y-Achse (rechte Seite), um Teilnehmer separat zu zeigen.
    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df["num_athletes"],
        name="# of Athletes",
        mode="lines+markers",
        yaxis="y2",
        line=dict(color="white", width=3)
    ))

    # Layout config
    fig.update_layout(
        title=f"Olympische Teilnahme & Medaillen ({start_year}–{end_year}) – {'Frau' if gender == 'F' else 'Mann'} Athleten",
        xaxis_title="Jahr",
        xaxis=dict(
            title="Year",
            tickmode="linear",
            dtick=4 
        ),
        yaxis=dict(title="Anzahl der Medaillen"),
        yaxis2=dict(title="Anzahl der Athleten", overlaying="y", side="right"),
        legend_title="",
        height=600
    )

    st.plotly_chart(fig)