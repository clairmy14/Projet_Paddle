import streamlit as st
from PIL import Image 
import pandas as pd
from bibliotheque.lib import *
from bibliotheque.base_donnees import *
from plotly import graph_objects as go
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter, FixedLocator

formatage_de_la_page("style.css")

entete_de_page()

st.subheader("Supprimer un salarié", divider='rainbow')

# création de la sidebar
st.sidebar.header("2 filtres sont nécessaires")
reset = st.sidebar.button("Réinitialiser les filtres")
if reset:
    reset_filtres_modifier()

st.sidebar.subheader("1er filtre")
nom_employe = st.sidebar.text_input('Quel nom?', key="nom_employe")
if not nom_employe:
    st.write("Saisissez le nom de l'employé à supprimer dans le 1er filtre")

    
st.sidebar.subheader("2ème filtre")
id_employe = st.sidebar.number_input('Quel id?', value=0, key="id_employe")

# le body de ma page
mes_colonnes = ["id_em", "nom", "prenom", "date_naissance", "date_entree", "date_sortie", "genre", "site","age"]

df = pd.DataFrame(question_8(), columns = mes_colonnes)
# df.set_index("id_em", inplace= True)       soucis avec mon 2ème filtre, à revoir avec iloc?

if nom_employe:
    df = df[df["nom"] == nom_employe]
    st.write ("Indiquez l'id_em retenu dans le 2ème filtre")

if id_employe:
    df = df[df["id_em"] == id_employe]
    activer = st.toggle("activer pour supprimer le formulaire")

    if activer:
            
        requete = f"DELETE FROM employes WHERE id_em = '{id_employe}' "
        se_connecter(requete)
            


st.write(df)


pied_de_page()