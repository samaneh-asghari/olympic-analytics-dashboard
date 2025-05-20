import data_access as da
import streamlit as st
from reports import report_1_top_x as rpt1
from reports import report_2_gender_teilnehmen as rpt2
from reports import report_3_avg_weight_height as rpt3
from reports import report_4_sport_alter_dist as rpt4
from reports import report_5_top_country_by_medal as rpt5

st.title("Olympic Games Data Dashboard - Asghari")

db = da.DataAccess()

#Aufruf der einzelnen Reports nacheinander

rpt1.list_top_countries_by_total(db)

st.divider()

rpt2.gender_teilnehmen_medal(db)

st.divider()

rpt3.report_avg_height_weight(db)

st.divider()

rpt4.report_sport_alter_dist(db)

st.divider()

rpt5.top_country_by_medal(db)

