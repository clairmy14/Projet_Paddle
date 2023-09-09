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

st.subheader("RGPD", divider='rainbow')

st.markdown('<a href="https://www.economie.gouv.fr/entreprises/reglement-general-protection-donnees-rgpd">"On va dire que je ne suis pas concernée."</a>' , unsafe_allow_html=True)


st.write("""
         Ce site est destiné exclusivement au service du personnel, 
         il s'agit d'un outil permettant de mieux traiter des données à caractères personnels 
         pour lesquels un registre a déjà été établi par l'entreprise.
         
         """)

st.markdown(f'<p style="text-align: center">Pour toute question, veuillez vous adresser au DPO de votre entreprise.</p>', unsafe_allow_html=True)


pied_de_page()