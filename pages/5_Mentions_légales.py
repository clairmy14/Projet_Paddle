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

st.subheader("Mentions légales", divider='rainbow')

st.markdown('<a href="https://www.economie.gouv.fr/entreprises/site-internet-mentions-obligatoires#">"On va dire que je suis une personne physique."</a>' , unsafe_allow_html=True)
monDico = {
            "Mon identité": ["Claire-Marie Foiret", "https://www.linkedin.com/in/claire-marie-foiret-8a7319274"],
            "Mes coordonnées": ["Cefim de Tours (37)" , "https://www.cefim.eu"],
            "Propriété intellectuelle": ["Sans doute libre, logo non trouvé avec google sur Unsplash/Pixabay/Pexels", "https://www.atoutnautic.fr/paddle-rigide/, https://www.atoutnautic.fr/mentions-legales/"],
            "Hébergement du site": ["Intranet de l'entreprise", "https://streamlit.io/cloud"]

} 

df = pd.DataFrame(monDico, index=["Descrition","Complément"]).T

st.write(df)




pied_de_page()