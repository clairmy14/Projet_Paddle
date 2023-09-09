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
st.subheader("Ajouter un salarié", divider='rainbow')


# Créer le formulaire avec la clé "my_form".
# with st.form(key="my_form", clear_on_submit=True):
st.write('Remplissez le formulaire suivant pour insérer un nouvel employé dans la base de données puis pressez le bouton "Submit".')
my_form = st.form(key="my_form", clear_on_submit=True)


# Créer les widgets pour saisir les informations de l'employé.
nom = my_form.text_input("Quel est son nom de famille?", key="nom")
prenom = my_form.text_input("Quel est son prénom?", key="prenom")
date_naissance = my_form.date_input("Quelle est sa date de naissance?", format= "YYYY-MM-DD", key="naissance")
date_entree = my_form.date_input("Quelle est sa date d'entrée?", format= "YYYY-MM-DD", key="entree")
    
col1, col2 = st.columns(2)
with col1:
    genres = ["Femme","Homme"]
    genre = my_form.radio("Quel est son genre?", genres,index = 1,key="genre")
with col2:
    sites = ["Blois","Bourges","Orléans","Tours"]
    site = my_form.radio("Quel est son site?", sites,index = 1,key="site")

# Créer le bouton "Submit" du formulaire.
submitted = my_form.form_submit_button("Submit" )

if genre == "Femme":
    genre = 1
else:   
    genre = 2

if site == "Orléans":
    site = 1
elif site == "Blois":
    site = 2
elif site == "Tours":
    site = 3
else:
    site = 4

# Si le bouton "Submit" est pressé, exécuter le code SQLITE pour insérer l'employé dans la base de données.
if submitted:
    reponse = "'" + "','".join([nom, prenom, date_naissance.strftime("%Y-%m-%d"), date_entree.strftime("%Y-%m-%d"), str(genre), str(site)]) + "'"
    # st.write(reponse)
    
    requete = f"INSERT INTO employes (nom, prenom, date_naissance, date_entree,id_ge,id_si) VALUES ({reponse})"
    se_connecter(requete)
    



pied_de_page()