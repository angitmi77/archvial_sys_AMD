import streamlit


def site_function():
    streamlit.title("Centres de recherche : ")
    streamlit.markdown("<br />" * 3, unsafe_allow_html=True)
    streamlit.write("---")

    research_centers = [
        ("Centre de recherche de l’UNICEF", "https://www.unicef-irc.org/"),
        ("Centre de recherche Banque Mondiale", "https://www.banquemondiale.org/fr"),
        ("Centre de recherche de la BAD", "https://www.afdb.org/fr"),
        ("Centre de recherche FMI", "https://www.imf.org/fr/Home"),
        ("Centre de recherche BIT", "https://www.ilo.org/global/about-the-ilo/who-we-are/international-labour-office/lang--fr/index.htm"),
        ("Centre de recherche de l’UNESCO", "https://www.unesco.org/fr"),
        ("Centre de recherche du PNUD", "https://www.undp.org/fr"),
        ("Centre de recherche OMS", "https://www.who.int/fr"),
        ("Centre de recherche de FAO", "https://www.fao.org/home/fr"),
        ("Centre de recherche de l’USAID", "https://www.usaid.gov/"),
        ("Centre de recherche de L’UE", "https://european-union.europa.eu/index_fr"),
        ("Centre de recherche du PAM", "https://fr.wfp.org/"),
        ("Centre de recherche de l’OIT", "https://www.ilo.org/global/lang--fr/index.htm"),
        ("Centre de recherche du HCR", "https://www.unhcr.org/fr"),
        ("Centre de recherche de l’UNFPA", "https://www.unfpa.org/fr")
    ]


    for center_name, center_link in research_centers:
        streamlit.write(f"### {center_name}")
        streamlit.write(f"[Visiter]({center_link})")
        streamlit.markdown("---")  # Horizontal line for separation