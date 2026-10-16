import streamlit as st
import pandas as pd

st.set_page_config(page_title="Charts",page_icon="📋")
st.sidebar.success("séléctionnez une page audessus")

df = pd.read_csv("././outputs/simulation.csv")

st.write("# Statistiques de la simulation de virus")
st.dataframe(df)

st.markdown("---")
st.write("## Graphiques de la simulation de virus")

st.line_chart(df, x="Jour", y=["Nombre d'agents infectés", "Nombre d'agents rétablis", "Nombre d'agents sains"], color=["red","blue","green"])