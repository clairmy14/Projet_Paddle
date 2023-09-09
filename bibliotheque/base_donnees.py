import streamlit as st
from PIL import Image 
import pandas as pd
import numpy as np
import sqlite3


def connecter():
    """
    :name : connecter
    :param : 
    :return : curseur et connexion nécessaires à d'autres fonctions
    :desc : se connecter à la base et activer le curseur
    """

    try:
        connexion = sqlite3.connect("Gestion_personnel.db")
        curseur = connexion.cursor()
        return curseur, connexion

    except sqlite3.Error as e:
        print(e, "\n\n=====> La connexion ne s'est pas établie")

def lire_reponse(resultats):
    
    """
    :name : lire_reponse
    :param : 
    :return : reponses
    :desc : afficher l'ensemble des réponses (ce qui sort du fetchall() est un NoneType, impossible à slicer)
    """
    
    reponses = []
    
    for resultat in resultats:
        
        reponses.append(resultat)
        
    return reponses


def se_connecter(requete):
    """
    :name : se_connecter
    :param : requete permettant de passer une instruction en sql
    :return : 
    :desc : la base va se connecter et se déconnecter à chaque passage de requête
    """

    try:
    
        connexion = sqlite3.connect("Gestion_personnel.db")
        curseur = connexion.cursor()
        curseur.execute(requete)
        connexion.commit()
        st.success("L'action s'est bien réalisée.")
        curseur.close()
        connexion.close()
    
    except sqlite3.Error as e:
        st.write(e)
        st.warning( "\n\n=====> Une action ne s'est pas réalisée (connexion, exécution ou déconnexion)")


def rechercher_employe():
    
    """
    :name : rechercher_employe
    :param : 
    :return : le nombre de résultat et le dernier résultat
    :desc : rechercher le nom d'un employé en tenant compte de la casse. 
            cette fonction est utile aux fonctions modifier_employe et supprimer_employe
    """
    
    
    try:
        curseur, connexion = connecter()


        nom_employe = input("Quel nom cherchez-vous? ")

        requete = f"SELECT *  FROM employes WHERE nom = '{nom_employe}' "
        resultats = curseur.execute(requete)

        
        nb_res = 0
        

        for resultat in resultats:
            print(f" {resultat}\t *** id_em = {resultat[0]} ***")
            nb_res += 1
        print(f"{nb_res} employé(s) porte le nom {nom_employe}")

        deconnecter(curseur,connexion)
        
        if nb_res > 0:
            
            return nb_res, resultat[0]
        
    
    except sqlite3.Error as e:
        print(e, "\n\n=====> La recherche de votre employé a échoué.")

def afficher_employe(id_em):
    
    """
    :name : afficher_employe
    :param : identifiant de l'employé
    :return : la fiche de l'employé
    :desc : afficher simplement la fiche de l'employé. 
            cette fonction est utile aux fonctions modifier_employe et supprimer_employe
    """
    
    try:
        curseur, connexion = connecter()
        
        requete = f"SELECT *  FROM employes WHERE id_em = '{id_em}'  "
        resultat = curseur.execute(requete)

        fiche_employe = []

        for res in resultat:
            fiche_employe.append(res)
            # print(fiche_employe)

        deconnecter(curseur,connexion)

        
        return fiche_employe


    except sqlite3.Error as e:
        print(e,"\n\n=====> L'affichage de votre employé a échoué.")

def colonne_table():
    
    """
    :name : colonne_table
    :param : 
    :return : la liste des noms de colonne dans la table employes
    :desc : créer une liste pour être afficher dans la fonction modifier_employe
    """
    
    
    try:
        curseur, connexion = connecter()


        requete = "PRAGMA table_info (employes);  "
        resultat = curseur.execute(requete)

        fiche_colonne = []

        for res in resultat:
            fiche_colonne.append(res)
            # print(fiche_employe)

        deconnecter(curseur,connexion)


        return fiche_colonne

    except sqlite3.Error as e:
        print(e, "\n\n=====> La création de la liste des colonnes a échoué")

def modifier_employe():
    
    
    """
    :name : modifier_employe
    :param : 
    :return : l' argument de la fonction se_connecter
    :desc : modifier la fiche d'un employé après l'avoir l'avoir cherchée et affichée
    """
    
    
    resultat = rechercher_employe()
    
    
    if resultat is not None:
           
        nb_res, last_res = resultat
        
        if nb_res != 1:
            last_res = input("Saisissez l'identifiant *** id_em *** de l'employé à modifier: ")


        fiche_employe = afficher_employe(last_res)

        print(f"=====> Vous allez travailler sur la fiche {fiche_employe} ")
        confirmation = confirmer()


        if confirmation:
            fiche_colonne = colonne_table()
            nouvelle_fiche_employe =[]

            for num,fiche in enumerate (fiche_colonne):
                if num == 0:
                    pass
                else:
                    print(f"Le champs {fiche_colonne[num][1]} donne {fiche_employe[0][num]}")
                    confirmation = confirmer()
                    if confirmation:
                        nouvelle_fiche_employe.append(fiche_employe[0][num])
                    else:
                        if "date" in fiche_colonne[num][1]:
                            nouvelle_fiche_employe.append(saisir_date())
                        else:
                            nouvelle_fiche_employe.append(input("Par quoi voulez-vous le remplacer? "))


            nv_nom,nv_prenom,nv_date_naissance,nv_date_entree,nv_date_sortie,nv_genre,nv_site = nouvelle_fiche_employe

            requete = f"UPDATE employes SET nom = '{nv_nom}', \
                                            prenom = '{nv_prenom}', \
                                            date_naissance = '{nv_date_naissance}', \
                                            date_entree = '{nv_date_entree}', \
                                            date_sortie = '{nv_date_sortie}', \
                                            id_ge = '{str(nv_genre)}', \
                                            id_si = '{str(nv_site)}' \
                                        WHERE id_em = '{last_res}' "




            print(requete)
            return requete

def question_1():
    
    """
    :name : question_1
    :param : 
    :return : le résultat de la requête
    :desc : afficher l'effectif de la société (employé non sorti des effectifs).
    """
    
    try:
    
        curseur, connexion = connecter()

        curseur.execute("""
                        SELECT count(*)  
                        FROM employes 
                        WHERE date_sortie is null
                        
                        """
                       )
        resultat = curseur.fetchall()
        return resultat
    
        deconnecter(curseur,connexion)
    
    except sqlite3.Error as e:
        print(e,"\n\n=====> L'affichage de la réponse a échoué.")

def question_2():
    
    """
    :name : question_2
    :param : 
    :return : le résultat de la requête
    :desc : afficher l'effectif de la société par site (employé non sorti des effectifs).
    """
    
    
    try:
    
        curseur, connexion = connecter()

        curseur.execute("""
                        SELECT site, count(*)  
                        FROM employes 
                            LEFT JOIN sites ON employes.id_si = sites.id_si
                        WHERE date_sortie is null
                        GROUP BY site
                        
                        """
                       )

        resultat = curseur.fetchall()
        return resultat
    
        deconnecter(curseur,connexion)
    
    except sqlite3.Error as e:
        print(e,"\n\n=====> L'affichage de la réponse a échoué.")

def question_6():
    
    """
    :name : question_6
    :param : 
    :return : le résultat de la requête
    :desc : trouver l'effectif par genre de la société (employé non sorti des effectifs)
    """
    
    try:
    
        curseur, connexion = connecter()

        curseur.execute("""
                        SELECT genre, count(*)
                        FROM employes 
                            LEFT JOIN genres ON employes.id_ge = genres.id_ge
                            
                        WHERE date_sortie is null
                        GROUP BY genre
                        
                        """
                       )

        resultat = curseur.fetchall()
        return resultat
    
        deconnecter(curseur,connexion)
    
    except sqlite3.Error as e:
        print(e,"\n\n=====> L'affichage de la réponse a échoué.")

def question_3b():
    
    """
    :name : question_3b
    :param : 
    :return : le résultat de la requête
    :desc : lister les âges des employés de la société (employé non sorti des effectifs) 
            pour réaliser le calcul de la médianne
    """
    
    try:
    
        curseur, connexion = connecter()

        curseur.execute("""
                        SELECT ROUND(((julianday(date()) - julianday(date_naissance))/365.25),1) as age
                        FROM employes 
                        
                        WHERE date_sortie is null
                        
                        ORDER BY age
                        
                        """
                       )

        resultat = curseur.fetchall()
        return resultat
    
        deconnecter(curseur,connexion)
    
    except sqlite3.Error as e:
        print(e,"\n\n=====> L'affichage de la réponse a échoué.")    

def deconnecter(curseur,connexion):
    
    """
    :name : deconnecter
    :param : curseur et connexion retournés par la fonction connecter()
    :return : 
    :desc : désactiver le curseur et se déconnecter de la base
    """ 
    
    try:
        curseur.close()
        connexion.close()
    except sqlite3.Error as e:
        print(e, "\n\n=====> La déconnexion ne s'est pas réalisée")

def question_8():
    
    """
    :name : question_8
    :param : 
    :return : le résultat de la requête
    :desc : afficher la liste de tous les employés de la société
    """
    
    try:
    
        curseur, connexion = connecter()

        curseur.execute("""
                        SELECT id_em, nom, prenom, date_naissance, date_entree, date_sortie, genre, site,
                        ROUND(((julianday(date()) - julianday(date_naissance))/365.25),1) as age
                        FROM employes 
                            LEFT JOIN genres ON employes.id_ge = genres.id_ge
                            LEFT JOIN sites ON employes.id_si = sites.id_si
                        
                        ORDER BY nom, prenom
                        
                        """
                       )

        resultat = curseur.fetchall()
        return resultat
    
        deconnecter(curseur,connexion)
    
    except sqlite3.Error as e:
        print(e,"\n\n=====> L'affichage de la réponse a échoué.")