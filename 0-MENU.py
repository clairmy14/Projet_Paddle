import streamlit as st
from PIL import Image 
import pandas as pd
from bibliotheque.lib import *
from bibliotheque.base_donnees import *
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter, FixedLocator

# toujours au début 
st.set_page_config(
    page_title="Gestion_personnel",
    page_icon="🧊",
    menu_items={
        'Get Help': 'https://www.cefim.eu',
        'About' : 'https://www.linkedin.com/in/claire-marie-foiret-8a7319274'}
        )

# prévoir de faire du st.pages pour améliorer le menu


# débuter la page
formatage_de_la_page("style.css")
entete_de_page()


col1, col2 = st.columns(2)

with col1:
    st.write(":female-technologist: :blue[Nombre de salariés] :man-rowing-boat:")

    with st.container():
        st.metric("", lire_reponse(question_1())[0][0])

with col2:
    st.write(":boy: :blue[Répartition par genre] :girl:")
    rep_genre = lire_reponse(question_6())
    mon_index=[]
    mes_valeurs=[]
    mon_dico = {}
    for i in range (len(rep_genre)):
        mon_index.append(rep_genre[i][0])
        mes_valeurs.append(rep_genre[i][1])
        mon_dico[rep_genre[i][0]] = rep_genre[i][1]

    plt.figure(figsize=(0.2,0.2))
    df = pd.DataFrame(mon_dico, index=["Nombre"]).T
    fig, ax = plt.subplots(figsize = (10,6))
    ax.pie(df['Nombre'], labels=df.index,autopct='%1.1f%%', colors = ["violet", "cornflowerblue"],
           wedgeprops={"linewidth": 1, "edgecolor": "white"})
    st.pyplot(fig)



col3, col4 = st.columns(2)

with col3:
    st.write(":baby: :blue[Répartition par tranche d'âges] :older_adult:")

    rep_age = lire_reponse(question_3b())

    mes_valeurs=[]
    for i in range (len(rep_age)):
        mes_valeurs.append(rep_age[i][0])
   
    df = pd.Series(data=mes_valeurs)

    colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(df)))

    fig, ax = plt.subplots(figsize = (6,6))
    ax.hist(df, bins = 9, linewidth = 1, edgecolor = "white",
            orientation="horizontal")

    ax.set_ylabel("âge")
    ax.set_xlabel("Nombre")

    ax.yaxis.set_major_locator(FixedLocator(np.arange(0, 100,1)))
    ax.xaxis.set_major_locator(FixedLocator(np.arange(0, 100,1)))

    st.pyplot(fig)



with col4:
    st.write(":cityscape: :blue[Répartition par ville] :factory: ")
    rep_ville = lire_reponse(question_2())
    
    mon_dico = {}
    for i in range (len(rep_ville)):
        
        mon_dico[rep_ville[i][0]] = rep_ville[i][1]

    plt.figure(figsize=(1,1))
    df = pd.DataFrame(mon_dico, index=["Nombre"]).T
    fig, ax = plt.subplots(figsize = (10,6))
    ax.pie(df['Nombre'], labels=df.index,autopct='%1.1f%%',
           wedgeprops={"linewidth": 1, "edgecolor": "white"})

    st.pyplot(fig)



pied_de_page()

