import streamlit as st
from PIL import Image 
import pandas as pd
from bibliotheque.lib import *
from bibliotheque.base_donnees import *
# from plotly import graph_objects as go
# import matplotlib.pyplot as plt
# from matplotlib.ticker import NullFormatter, FixedLocator
import datetime


formatage_de_la_page("style.css")

entete_de_page()
st.subheader("Afficher les salariés", divider='rainbow')


# création de la sidebar
st.sidebar.header("4 filtres sont disponibles")
reset = st.sidebar.button("Réinitialiser les filtres")
if reset:
    reset_filtres_afficher()



st.sidebar.subheader("1er filtre")

ageMini, ageMaxi = st.sidebar.select_slider(
    'Entre quels âges?',
    # options=[16,24,44,54,64],
    options=range(16,81),
    value=(16, 80),
    key=("ageMini,ageMaxi"))


st.sidebar.subheader("2ème filtre")

st.sidebar.write("Quels genres?")
genreFemme = st.sidebar.checkbox('Femme', value=True, key="genreFemme")
genreHomme = st.sidebar.checkbox('Homme', key="genreHomme")

 
st.sidebar.subheader("3ème filtre")

sites = ["Blois","Bourges","Orléans","Tours"]
sites = st.sidebar.multiselect(
    'Quels sites?',
    sites,
    # ['Tours'],
    placeholder="Tous les sites",
    key="sites")


st.sidebar.subheader("4ème filtre")

periode1 = st.sidebar.selectbox(
    'Sur quelle période? ',
    ('jusque', 'depuis'),
    key="periode1")
# jourRef = st.sidebar.date_input("le", datetime.date(2019, 7, 6),key="jourRef")   
jourRef = st.sidebar.date_input("le", datetime.date.today(),key="jourRef")   
periode2 = st.sidebar.selectbox(
    'sur la date de ',
    ('entrée', 'sortie'),
    key="periode2")


st.write(f'''
         Vous souhaitez afficher le personnel qui a entre {ageMini} et {ageMaxi} ans, 
         dont le genre est Femme {genreFemme} et Homme {genreHomme} sinon tous,
         pour la période {periode1} le {jourRef} sur la date de {periode2},
         dont le site est {sites} sinon tous.
         ''')

 

# le body de ma page
mes_colonnes = ["id_em", "nom", "prenom", "date_naissance", "date_entree", "date_sortie", "genre", "site","age"]

df = pd.DataFrame(question_8(), columns = mes_colonnes)
df.set_index("id_em", inplace= True)


if sites:
    df = df[df["site"].isin(sites)]

# j'ai fait les cases à cocher comme demandé mais pas pratique
# Si on a d'autres genres, on pourra toujours ne sélectionner que les hommes et les femmes
if genreFemme and not genreHomme:
    df = df[df["genre"] == "Femme"]
if genreHomme and not genreFemme:
    df = df[df["genre"]== "Homme"]

if ageMini and ageMaxi:
    df = df[(df["age"]>= ageMini) & (df["age"]<= ageMaxi)]


if periode1 == "jusque" and periode2 =="entrée":
    # st.write("base", df["date_entree"],"form",str(jourRef))
    df = df[df["date_entree"]<= str(jourRef)]

if periode1 == "depuis" and periode2 =="entrée":
    df = df[df["date_entree"]>= str(jourRef)]


if periode1 == "jusque" and periode2 =="sortie":
    df = df[df["date_sortie"]<= str(jourRef)]

if periode1 == "depuis" and periode2 =="sortie":
    df = df[df["date_sortie"]>= str(jourRef)]




st.write(df)


pied_de_page()




