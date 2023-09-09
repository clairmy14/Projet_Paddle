import streamlit as st
from PIL import Image 
import pandas as pd
import numpy as np
# pip install pysqlite3
import sqlite3
import datetime

def entete_de_page():

    # contexte = '''Vous travaillez pour une société de vente de paddle. Cette société est implantée en région Centre-Val-de-Loire dans les villes d’Orléans, Blois, Tours et Bourges. Vos missions au sein de la DSI portent sur l’analyse de données et le développement d’applications permettant de traiter des données.
    # '''

    colonne_logo, colonne_titre = st.columns((1,7))
    with colonne_logo:
            logo = Image.open("images/image_paddle.jpg") 
            logo_reduit = logo.resize((200,200))
            st.image(logo_reduit)

    with colonne_titre:
            st.subheader("Application de gestion du personnel")

    #st.write(contexte)
    st.divider()


    # pour désactiver le message “Made with Streamlit” et le menu hamburger https://github.com/streamlit/streamlit/issues/892
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

def pied_de_page():
    st.divider()

    with st.container():
        st.markdown('<div id="href"><a href="Mentions_légales" target="_self">Mentions légales</a> | <a href="RGPD" target="_self">RGPD</a></div>' , unsafe_allow_html=True)

def reset_filtres_afficher():

    st.session_state["ageMini,ageMaxi"] = (16,80)

    st.session_state["genreFemme"] = True
    st.session_state["genreHomme"] = False
    
    st.session_state["sites"] = []

    st.session_state["periode1"] = 'jusque'
    st.session_state["jourRef"] = datetime.date.today()
    st.session_state["periode2"] = 'entrée'

def reset_filtres_modifier():

    
    st.session_state["nom_employe"] = ""
    st.session_state["id_employe"] = 0

def formatage_de_la_page(fichier_css):
    with open(fichier_css) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def charger_le_fichier_de_donnees1():
    """
    Nom : charger_le_fichier_de_donnees
    Paramètre : 0
    Traitement : charger un fichier au format csv grâce à file_uploader
    Retour : retourne le fichier csv dans la variable fichier_charge
    """
    fichier_charge1 = st.file_uploader("Choisissez votre 1er fichier csv", 
                                      type=["csv"])
    if fichier_charge1:
        st.write(f"Vous venez de charger le fichier : {fichier_charge1.name}.")
    return(fichier_charge1)

def charger_le_fichier_de_donnees2():
    """
    Nom : charger_le_fichier_de_donnees
    Paramètre : 0
    Traitement : charger un fichier au format csv grâce à file_uploader
    Retour : retourne le fichier csv dans la variable fichier_charge
    """
    fichier_charge2 = st.file_uploader("Choisissez votre 2nd fichier csv", 
                                      type=["csv"])
    if fichier_charge2:
        # st.write(f"Vous venez de charger le fichier : {fichier_charge2.name}.")
        st.write(f"Vous venez de charger le fichier : {fichier_charge2.name}.")
    return(fichier_charge2)

def creer_le_jeu_de_donnees(f_fichier_au_format_csv):
    """
    Nom : creer_le_jeu_de_donnees
    Paramètre : 1 - Type : chaîne de caractères
    Traitement : charger un dataset à partir d'un fichier csv
    Retour : retourne le dataset dans la variable dataset
    """
    dataset = pd.read_csv(f_fichier_au_format_csv, 
                        encoding="latin", sep=";")
    st.write("Le jeu de données a bien été chargé, voici les 3 ères lignes.")
    st.write(dataset.head(3))
    return(dataset)

def rechercher_par_code_postal(f_jeu_de_donnees):
    """
    Nom : rechercher_par_code_postal
    Paramètre : 1 - Type : chaîne de caractères
    Traitement : afficher un champ de recherche
    Retour : retourne le jeu de données dont les données correspondent au code postal
    """
    f_jeu_de_donnees['code_postal'] = f_jeu_de_donnees['code_postal'].apply(str)
    recherche_code_postal = st.text_input("Tapez un code postal 👇", 
                                      max_chars=5,
                                      help="Tapez un code postal commençant par 37", 
                                      placeholder="Code postal en 37")
    try :
        if recherche_code_postal:
            st.write(f_jeu_de_donnees[f_jeu_de_donnees["code_postal"] == recherche_code_postal])
    except:
        st.write("La recherche tapée n'est pas correcte.")

def rechercher_par_nom_assos(f_jeu_de_donnees):
    """
    Nom : rechercher_par_code_postal
    Paramètre : 1 - Type : chaîne de caractères
    Traitement : afficher un champ de recherche
    Retour : retourne le jeu de données dont les données correspondent au code postal
    """
    
    recherche_nom_assos = st.text_input("Tapez un nom 👇", 
                                      max_chars=40,
                                      help="Tapez un mot contenu dans le nom de l'association", 
                                      placeholder="nom de l'association en MAJUSCULE non accentuée")
    try :
        if recherche_nom_assos:
            st.write(f_jeu_de_donnees[f_jeu_de_donnees["nom_asso"].str.contains(recherche_nom_assos) ])
    except:
        st.write("La recherche tapée n'est pas correcte.")

def nettoyer_le_jeu_de_donnees(f_jeu_de_donnees):
    # Récupération du fichier groupe réalisé par Awatef pour l'intégrer dans ma fonction et y faire quelques arrangements.

    print(f"La version de streamlit est {st.__version__}")

    df = pd.DataFrame(f_jeu_de_donnees)
    st.write(f"Le tableau initial contient {df.shape[0]} lignes et {df.shape[1]} colonnes.")

    # 1. Obtiens la liste des libellés de colonnes
    st.write(f" Voici la liste des colonnes initiales: {df.columns.tolist()}.")

    # 2. Choisis les index des colonnes à supprimer
    indexes_a_supprimer = [1,3,4,6,7,10,12,13,15,16,17,18,19,20,21,24,26,27,28,29,30,31,32,33, 35,36,38]
    df.drop(df.columns[indexes_a_supprimer], axis=1, inplace=True)
    st.write(f" Voici la liste des colonnes retenues: {df.columns.tolist()}.")
    st.write(f"Le tableau retenu contient {df.shape[0]} lignes et {df.shape[1]} colonnes.")

    # Renommer les colonnes
    nouveaux_noms = {
        'titre': 'nom_asso',
        'objet_social1': 'objet_social_id',
        'adrs_codeinsee': 'code_commune_INSEE',
        'adrs_codepostal': 'code_postal',
        'adrg_declarant': 'nom_declarant',
        'adrg_codepostal': 'code_postal_declarant',
        'adrg_achemine': 'nom_ville',
        'position': 'statut_activite'
        # Ajoute d'autres correspondances ici
    }

    # Renomme les colonnes en utilisant le dictionnaire de correspondance
    df.rename(columns=nouveaux_noms, inplace=True)
    st.write(f" Voici la liste des colonnes renommées: {df.columns.tolist()}.")



    tab1, tab2 = st.tabs([":blue[Avant correction des types]",":blue[Après correction des types]"])
    with tab1:
        st.write(df.dtypes)
    with tab2:
        # Convertir les colonnes en chaînes de caractères et garder les 10 premiers caractères
        df['id'] = df['id'].astype(str).str[:10]

        # Convertir les colonnes "date_creat" et "date_disso" au format JJ/MM/AAAA
        df['date_creat'] = pd.to_datetime(df['date_creat'], errors='coerce') # format='%Y%m%d'
        df['date_disso'] = pd.to_datetime(df['date_disso'], errors='coerce')
        

        # Convertir les colonnes en chaînes de caractères et garder les 5 premiers caractères
        df['code_postal'] = df['code_postal'].astype(str).str[:5]
        df['code_commune_INSEE'] = df['code_commune_INSEE'].astype(str).str[:5]

        # Convertir la colonne "siret" en chaînes de caractères
        df['siret'] = df['siret'].apply(str).str[:14]   # je mets apply à la place de astype

        # Convertir la colonne "objet_social_id" en chaînes de caractères
        #df['objet_social_id'] = df['objet_social_id'].apply(str).str[:5]   # je mets apply à la place de astype

        # Afficher les types de données mis à jour
        st.write(df.dtypes)

    tab3, tab4 = st.tabs([":blue[dtype des communes]",":blue[dtype des objets]"])
    with tab3:
        # Charger les fichiers CSV dans les DataFrames
        df_communes = pd.read_csv("source//communes-departement-region.csv", encoding="utf8", sep=",")
        st.write(df_communes.dtypes)
    with tab4:
        df_objet_parent = pd.read_csv("source//rna-associations-nomenclature-waldec.csv", encoding="utf8", sep=";")
        st.write(df_objet_parent.dtypes)


    # Fusionner les DataFrames en utilisant la colonne "code_postal" comme clé
    merged_df = df.merge(df_communes[["code_commune_INSEE", "latitude", "longitude"]],
                        on="code_commune_INSEE",
                        how="left")

    # Fusionner les DataFrames en utilisant la colonne "objet_social_id" comme clé
    merged_df = merged_df.merge(df_objet_parent[["objet_social_id", "objet_social_parent_lib"]],
                                on="objet_social_id",
                                how="left")

    # Renommer la colonne fusionnée pour plus de clarté
    merged_df.rename(columns={"objet_social_parent_lib": "objet_social_parent"}, inplace=True)

    # Afficher le DataFrame fusionné avec les colonnes ajoutées
    st.write(f" Voici la liste des colonnes après fusion: {merged_df.columns.tolist()}.")
    st.write(f"Le tableau fusionné contient {merged_df.shape[0]} lignes et {merged_df.shape[1]} colonnes.")

    # remplacer les nan
    merged_df.replace(np.nan, None, inplace=True)
    

    # Sauvegarder le DataFrame merged_df dans un fichier CSV
    merged_df.to_csv("datas/merged_df.csv", encoding="latin", sep=";", index=False)
    st.write("fichier sauvegardé")

    st.write(merged_df)


    # préparer le tableau final
    df_final = merged_df.copy()

    # 2. Choisis les index des colonnes à supprimer
    indexes_a_supprimer = [12,13]
    df_final.drop(columns=["latitude","longitude"], axis=1, inplace=True)
    df_final.drop_duplicates(inplace=True)

    
    st.write(f"Le tableau final contient {df_final.shape[0]} lignes et {df_final.shape[1]} colonnes.")
    df_final.to_csv("datas/df_final.csv", encoding="latin", sep=";", index=False)
    st.write("fichier sauvegardé")
    st.write(df_final)


    return (merged_df,df_final)









