import streamlit as st
import pandas as pd
import plotly.express as px
import data_access as da

def report_sport_alter_dist(db:da.DataAccess):
    st.subheader("🎯 Altersentwicklung von Medaillengewinner:innen in ausgewählten Sportarten")

    with st.expander("ℹ️ Worum geht es in dieser Visualisierung?"):
        st.write("""
        Dieses Balkendiagramm zeigt die **durchschnittlichen Alterswerte von Olympia-Medaillengewinner:innen** im gewählten Sport **über die Jahre hinweg** – aufgeteilt nach **Medaillenart** (Gold, Silber, Bronze).

        ### 📊 Was zeigt das Diagramm?
        - **x-Achse**: Olympiajahr
        - **y-Achse**: Durchschnittsalter der Medaillengewinner:innen
        - **Balkenfarben**: Art der Medaille (Gold, Silber, Bronze)
        - Die Balken sind **gruppiert**, sodass pro Jahr alle drei Medaillentypen nebeneinander dargestellt werden.

        ### 🔍 Erkenntnisse, die du aus dem Diagramm gewinnen kannst:
        - 🧓 Wie sich das Alter von erfolgreichen Athlet:innen in einem bestimmten Sport über die Jahrzehnte entwickelt hat
        - 👶 In welchen Jahren tendenziell jüngere oder ältere Athlet:innen erfolgreich waren
        - 🥇 Gibt es Unterschiede im Alter zwischen Gold-, Silber- und Bronzegewinner:innen?
        - ⏳ Identifikation von Sportarten, in denen Erfahrung (höheres Alter) oder Jugend (niedrigeres Alter) besonders wichtig ist

        📌 Nutze die Filter unten, um gezielt eine Sportart auszuwählen und die Altersverteilung zu analysieren
        """)


    sports=db.list_sports()
    
    # Dropdown zur Auswahl einer einzelnen Sportart mit Standardwert (Index 5), z. B. Badminton
    select_sport=st.selectbox("Eine Sportart auswählen", sports,5,key=7)

    data=db.list_sport_alter_dist(sport=select_sport)

    # Erstellt ein gruppiertes Balkendiagramm (Balken nebeneinander für jede Medaille)
    fig = px.bar(
        data,
        x="Year",
        y="avg_age",
        color="Medal",
        barmode="group",  
        title=f"Durchschnittsalter der Medaillengewinner in {select_sport} im Zeitverlauf",
        labels={
            "avg_age": "Durchschnittsalter",
            "Year": "Olympiajahr",
            "Medal": "Medaillenart"
        },
        color_discrete_map={
            "Gold": "#FFD700",    # Gold
            "Silver": "#C0C0C0",  # Silver
            "Bronze": "#CD7F32"   # Bronze
        },
    )

    # show all Olympic years/dtick=4 zeigt alle vier Jahre (Olympiajahre) an.
    fig.update_layout(xaxis=dict(dtick=4))  
    
    # Diagramm anzeigen und Containerbreite vollständig nutzen
    st.plotly_chart(fig, use_container_width=True)