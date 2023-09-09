import streamlit as st
from PIL import Image 
import pandas as pd
from bibliotheque.lib import *
from bibliotheque.base_donnees import *
from plotly import graph_objects as go
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter, FixedLocator
import datetime

formatage_de_la_page("style.css")

entete_de_page()

st.subheader("Modifier un salarié", divider='rainbow')



# création de la sidebar
st.sidebar.header("2 filtres sont nécessaires")
reset = st.sidebar.button("Réinitialiser les filtres")
if reset:
    reset_filtres_modifier()

st.sidebar.subheader("1er filtre")
nom_employe = st.sidebar.text_input('Quel nom?', key="nom_employe")
if not nom_employe:
    st.write("Saisissez le nom de l'employé à modifier dans le 1er filtre")

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
    activer = st.toggle("activer pour modifier le formulaire")

    if activer:
        
        # Créer le formulaire avec la clé "my_form".
        # with st.form(key="my_form", clear_on_submit=True):
        st.write('Remplissez le formulaire suivant pour modifier la fiche de votre employé dans la base de données puis pressez le bouton "Submit".')

        recup_nom = df[df["id_em"] == id_employe]["nom"].values[0]
        recup_prenom = df[df["id_em"] == id_employe]["prenom"].values[0]
        recup_date_naissance = df[df["id_em"] == id_employe]["date_naissance"].values[0]
        recup_date_entree = df[df["id_em"] == id_employe]["date_entree"].values[0]
        recup_date_sortie = df[df["id_em"] == id_employe]["date_sortie"].values[0]
        recup_genre = df[df["id_em"] == id_employe]["genre"].values[0]
        recup_site = df[df["id_em"] == id_employe]["site"].values[0]
        
        my_form = st.form(key="my_form", clear_on_submit=True)
        # Créer les widgets pour saisir les informations de l'employé.
        nom = my_form.text_input("Quel est son nom de famille?",recup_nom, key="nom")
        prenom = my_form.text_input("Quel est son prénom?",recup_prenom, key="prenom")
        date_naissance = my_form.text_input("Quelle est sa date de naissance?", recup_date_naissance,key="naissance")
        date_entree = my_form.text_input("Quelle est sa date d'entrée?",recup_date_entree, key="entree")
        date_sortie = my_form.text_input("Quelle est sa date de sortie?",recup_date_sortie, key="sortie")

        
        col1, col2 = st.columns(2)
        with col1:
            if recup_genre == 1:
                genre = "Femme"
            else:   
                genre = "Homme"

            genres = ["Femme","Homme"]
            genre = my_form.radio("Quel est son genre?", genres,index = genres.index(genre),key="genre")
        with col2:
            if recup_site == 1:
                site = "Orléans"
            elif recup_site == 2:
                site = "Blois"
            elif recup_site == 3:
                site = "Tours"
            else:
                site = "Bourges"

            sites = ["Blois","Bourges","Orléans","Tours"]
            site = my_form.radio("Quel est son site?", sites,index = sites.index(site),key="site")

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
            if date_sortie == "None":
                # reponse = "'" + "','".join([nom, prenom, date_naissance.strftime("%Y-%m-%d"), date_entree.strftime("%Y-%m-%d"), str(genre), str(site)]) + "'"
                requete = f"UPDATE employes SET nom = '{nom}', \
                                            prenom = '{prenom}', \
                                            date_naissance = '{date_naissance}', \
                                            date_entree = '{date_entree}', \
                                            id_ge = '{str(genre)}', \
                                            id_si = '{str(site)}' \
                                        WHERE id_em = '{id_employe}' "
            else:
                
                requete = f"UPDATE employes SET nom = '{nom}', \
                                            prenom = '{prenom}', \
                                            date_naissance = '{date_naissance}', \
                                            date_entree = '{date_entree}', \
                                            date_sortie = '{date_sortie}', \
                                            id_ge = '{str(genre)}', \
                                            id_si = '{str(site)}' \
                                        WHERE id_em = '{id_employe}' "
                       
            se_connecter(requete)
            




st.write(df)


pied_de_page()