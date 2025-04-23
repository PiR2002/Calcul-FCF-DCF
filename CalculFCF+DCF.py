import numpy as np
import pandas as pd
import streamlit as st

def calculate_dcf(fcf_list, wacc, g, start_year):
    """
    Calcule la valeur actuelle nette d'une entreprise avec la méthode DCF.

    :param fcf_list: Liste des Free Cash Flows projetés (ex: [100, 110, 121, ...])
    :param wacc: Taux d'actualisation (ex: 0.10 pour 10%)
    :param g: Taux de croissance à long terme (ex: 0.02 pour 2%)
    :param start_year: Année de début de projection (ex: 2025)
    :return: DataFrame avec les résultats et valeur totale du DCF
    """
    n_years = len(fcf_list)
    terminal_value = fcf_list[-1] * (1 + g) / (wacc - g)

    actualised_fcf = [fcf_list[i] / (1 + wacc) ** (i + 1) for i in range(n_years)]
    actualised_terminal_value = terminal_value / (1 + wacc) ** n_years

    dcf_total = sum(actualised_fcf) + actualised_terminal_value

    df = pd.DataFrame({
        "Année": [start_year + i for i in range(n_years)],
        "FCF": fcf_list,
        "FCF actualisé": actualised_fcf
    })

    df.loc[len(df.index)] = ["Valeur Terminale", terminal_value, actualised_terminal_value]
    df.loc[len(df.index)] = ["TOTAL DCF", "", dcf_total]

    return df, dcf_total

# Interface utilisateur Streamlit
st.title("Calculateur DCF - Discounted Cash Flow")

start_year = st.number_input("Année de départ", min_value=2000, max_value=2100, value=2025)
nb_years = st.slider("Nombre d'années de projection", 1, 10, 5)

fcf_list = []
for i in range(nb_years):
    fcf = st.number_input(f"FCF année {start_year + i} (en M€)", value=100 + i * 10)
    fcf_list.append(fcf)

wacc = st.slider("Taux d'actualisation (WACC)", 0.01, 0.20, 0.10, step=0.01)
g = st.slider("Taux de croissance à long terme (g)", 0.00, 0.10, 0.02, step=0.01)

if st.button("Calculer le DCF"):
    result_df, dcf_value = calculate_dcf(fcf_list, wacc, g, start_year)
    st.dataframe(result_df)
    st.success(f"Valeur DCF totale estimée : {dcf_value:.2f} M€")
