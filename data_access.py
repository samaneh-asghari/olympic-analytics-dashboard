import pandas as pd

class DataAccess:
    def __init__(self):

       self.athlete_events=pd.read_csv('data/athlete_event.csv' , delimiter=';')
       self.events=pd.read_csv('data/events.csv' , delimiter=';')
       self.countries=pd.read_csv('data/countries.csv' , delimiter=';').dropna(subset=['NOC','Country'])
       self.athletes=pd.read_csv('data/athletes.csv' , delimiter=';')


    def list_countries(self):
        result = dict(zip(self.countries['NOC'],self.countries['Country']))
        return result
    
    def list_sports(self):
        all_sports =sorted(self.events["Sport"].dropna().unique())
        return all_sports
    
    #limit: Anzahl der Länder (z. B. Top 10)
    #from_year, to_year: Jahresbereich
    #sports: Liste der Sportarten
    def list_top_countries_by_total_medal(self,limit: int, from_year: int, to_year: int, sports):
        #Nur Zeilen mit Medaillen (Gold, Silber, Bronze) und im angegebenen Jahresbereich
        whereResult = self.athlete_events[
            self.athlete_events['Medal'].isin(['Gold', 'Silver', 'Bronze']) & 
            self.athlete_events['Year'].between(from_year, to_year)]

        #Ergänzt die Sportart-Info über Join mit events
        whereResult=whereResult.merge(self.events, on='Event_ID', how="left")
        #Filtert zusätzlich nach ausgewählten Sportarten
        whereResult=whereResult[whereResult['Sport'].isin(sports)]

        #Verknüpft mit Ländernamen(Country) über NOC
        joinResult= whereResult.merge(self.countries, on='NOC', how='left')

        #Gruppiert nach Country und zählt alle Medaillenarten
        groupByResult = joinResult.groupby('Country').agg(
            Gesamtmedaillen=('Medal', lambda x: (x != '').sum()),
            Goldmedaillen=('Medal', lambda x: (x == 'Gold').sum()),
            Silbermedaillen=('Medal', lambda x: (x == 'Silver').sum()),
            Bronzemedaillen=('Medal', lambda x: (x == 'Bronze').sum())
        ).reset_index()

        #Sortiert absteigend nach Gesamtzahl und gibt die Top-Länder zurück
        result = groupByResult.sort_values(by='Gesamtmedaillen', ascending=False).head(limit)
        return result
    


    def list_teilnehmen_medal_by_gender(self, from_year: int, to_year: int, gender: str):

        joinResult = pd.merge(self.athlete_events, self.athletes, on="Athlete_ID")
        
        #Filtert die Daten
        whereResult = joinResult[
            (joinResult["Sex"] == gender) &
            (joinResult["Year"] >= from_year) &
            (joinResult["Year"] <= to_year)
        ]

        #Gruppiert nach Year und Berechnet: Anzahl einzigartiger Athleten pro Jahr /  Anzahl Goldmedaillen ,Silbermedaillen und Bronzemedaillen
        groupResult = whereResult.groupby("Year").agg(
            num_athletes=("Athlete_ID", pd.Series.nunique),
            num_gold=("Medal", lambda x: (x == "Gold").sum()),
            num_silver=("Medal", lambda x: (x == "Silver").sum()),
            num_bronze=("Medal", lambda x: (x == "Bronze").sum()),
        )
        groupResult["total_medals"] = (
            groupResult["num_gold"] + groupResult["num_silver"] + groupResult["num_bronze"]
        )

        # Konvertiert den Index(für Diagramme notwendig).
        result = groupResult.reset_index()
        return result

    #Verknüpft drei Tabellen
    def list_avg_weight_height(self,sports,sex):
        df = self.athlete_events.merge(self.events, on="Event_ID", how="left").merge(self.athletes, on="Athlete_ID", how="left")
        
        # Filtern der Daten
        filtered_df=df[
            (df["Medal"].isin(["Gold", "Silver", "Bronze"]))& 
            (df["Sex"].isin(sex))& 
            (df["Height"].notnull())&
            (df["Weight"].notnull())&
            (df["Sport"]).isin(sports)
        ]

        #Gruppiert nach Sportart und Geschlecht und Berechnet:Durchschnittliche & Durchschnittliches Gewicht &Anzahl der Medaillengewinner je Gruppe
        grouped_df=filtered_df.groupby(["Sport","Sex"]).agg(
            avg_height=("Height",lambda x: round(x.mean(),1)),
            avg_weight=("Weight",lambda x: round(x.mean(),1)),
            athlete_count=("Athlete_ID", "count")

        ).reset_index()

        grouped_df["avg_height"] = grouped_df["avg_height"]/10
        grouped_df["avg_weight"] = grouped_df["avg_weight"]/10

        return grouped_df
    
    #Filterung: Nur Medaillengewinner mit Altersangabe
    def list_sport_alter_dist(self, sport):
        df=self.athlete_events[
            self.athlete_events["Medal"].isin(['Gold', 'Silver', 'Bronze']) &
            self.athlete_events["Age"].notnull()]
        
        #Verknüpfen mit Events, um Sportarten zuordnen zu können
        df=df.merge(self.events , on="Event_ID", how="left")
        #Filterung auf die gewählte Sportart
        df = df[df['Sport']==sport]

        #Gruppierung nach:Sport,Jahr,Medaille &Berechnung des durchschnittlichen Alters
        grouped_df=df.groupby(["Sport","Year","Medal"])['Age'].mean().round(1)
       
        grouped_df=grouped_df.reset_index(name="avg_age")
        return grouped_df
    
    def list_top_country_by_medal(self, medal: str, limit: int):

        #Filtern auf den gewünschten Medaillentyp
        whereResult = self.athlete_events[self.athlete_events['Medal']==medal]

        joinResult = whereResult.merge(self.countries, on='NOC', how='left')

        #Gruppiert nach Country &Zählt, wie oft jede Nation eine Medaille des gewählten Typs gewonnen hat
        groupby = joinResult.groupby(['Country']).agg(
            Medals=('Medal', 'count')
        )

        #Sortiert absteigend nach Anzahl der Medaillen
        result = groupby.sort_values(by='Medals', ascending=False).head(limit).reset_index()
        return result


    